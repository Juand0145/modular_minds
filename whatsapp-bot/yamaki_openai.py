from openai import AzureOpenAI
from dotenv import load_dotenv
from typing import Tuple, Optional
import os
import uuid
from datetime import datetime

from yamaki_config import (
    PALABRAS_CLAVE_YAMAKI,
    ESCALAMIENTO,
    CANALES_ATENCION_YAMAKI,
    MARCAS,
)


load_dotenv()

azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")

client = AzureOpenAI(
    api_version="2023-05-15",
    azure_endpoint=azure_endpoint,
    api_key=api_key,
)


def _clean_json_fence(text: str) -> str:
    if not text:
        return ""
    cleaned = text
    if "```json" in cleaned:
        try:
            cleaned = cleaned.split("```json")[1].split("```")[0].strip()
        except Exception:
            pass
    elif "```" in cleaned:
        try:
            cleaned = cleaned.split("```")[1].strip()
        except Exception:
            pass
    return cleaned


def classify_yamaki(message: str) -> Optional[str]:
    """Clasifica el mensaje para Yamaki usando GPT.

    Devuelve un JSON en string con el siguiente formato:
    {
        "tipo_pqr": "Saludo/Petición/Queja/Reclamo/Solicitud",
        "categoria": "Bienvenida/Productos/Garantías/Soporte técnico/Distribuidores/Cotizaciones/Capacitaciones",
        "marca": "blackmagic|d&b audiotechnik|muxlab|presonus|fujifilm|kino flo|e-image|Otra",
        "asunto": "Resumen en ≤7 palabras",
        "descripcion": "Resumen en ≤20 palabras",
        "subcategoria": "Texto breve",
        "requires_human": true|false,
        "reason": "Motivo del escalamiento si aplica"
    }
    """

    brands_str = ", ".join(MARCAS)
    classification_prompt = f"""
Eres un asistente de clasificación de Yamaki (audio, video e iluminación profesional).

Mensaje del cliente:
"{message}"

Responde SOLO en formato JSON, sin texto adicional:
{{
  "tipo_pqr": "Saludo/Petición/Queja/Reclamo/Solicitud",
  "categoria": "Bienvenida/Productos/Garantías/Soporte técnico/Distribuidores/Cotizaciones/Capacitaciones",
  "marca": "{brands_str} | Otra",
  "asunto": "Resumen en ≤7 palabras",
  "descripcion": "Resumen en ≤20 palabras",
  "subcategoria": "Tema específico",
  "requires_human": true/false,
  "reason": "Si requires_human=true, explica brevemente"
}}

Reglas:
- Si es un saludo (hola, buenas, etc.), categoria="Bienvenida" y tipo_pqr="Saludo".
- Si menciona hablar con asesor, soporte técnico avanzado o cotización especial, requires_human=true.
- Si detectas una marca, colócala; si no, usa "Otra".
"""

    try:
        completion = client.chat.completions.create(
            model="UnosquareGPT4oModel",
            messages=[{"role": "user", "content": classification_prompt}],
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error en clasificación Yamaki: {e}")
        return None


def generate_response_yamaki(user_phone: str, message: str, classification_data: Optional[str]) -> Tuple[str, str, bool, str]:
    """Genera respuesta para Yamaki y devuelve (texto, pqr_id, requires_human, categoria).

    - Bienvenida: responde saludo corto
    - FAQ o solicitudes: respuesta breve con pasos y contacto
    - Si requires_human=True: mensajería de escalamiento
    """

    pqr_id = f"YMK-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
    requires_human = False
    categoria = ""

    # Defaults
    tipo_pqr = "Solicitud"
    asunto = "Consulta general"
    descripcion = message
    marca = "Otra"
    subcategoria = ""

    try:
        if classification_data:
            import json

            clean_json = _clean_json_fence(classification_data)
            class_data = json.loads(clean_json)
            tipo_pqr = class_data.get("tipo_pqr", tipo_pqr)
            categoria = class_data.get("categoria", "")
            marca = class_data.get("marca", marca)
            asunto = class_data.get("asunto", asunto)
            descripcion = class_data.get("descripcion", descripcion)
            subcategoria = class_data.get("subcategoria", "")
            # Ignorar requires_human del modelo; solo usaremos disparadores explícitos en app
            requires_human = False
    except Exception as e:
        print(f"Error parseando clasificación Yamaki: {e}")

    # Bienvenida
    if (categoria and categoria.lower() == "bienvenida") or (tipo_pqr and tipo_pqr.lower() == "saludo"):
        welcome = (
            "¡Hola! Soy el asistente virtual de Yamaki. "
            "Puedo ayudarte con productos, garantías, soporte técnico, distribuidores, cotizaciones y capacitaciones.\n\n"
            "¿En qué te puedo apoyar hoy?"
        )
        return welcome, "BIENVENIDA", False, "Bienvenida"

    # Respuesta corta y determinística para Garantías
    try:
        cat_norm = (categoria or "").lower()
        msg_norm = (message or "").lower()
        if ("garant" in cat_norm) or ("garant" in msg_norm):
            support_email = os.getenv("YAMAKI_SUPPORT_EMAIL", CANALES_ATENCION_YAMAKI.get("soporte"))
            brand_norm = (marca or "").strip()
            brand_text = f" de {brand_norm}" if brand_norm and brand_norm.lower() != "otra" else ""
            short_text = (
                f"Entiendo. Para iniciar el proceso de garantía{brand_text} necesitamos: marca, modelo, número de serie y factura.\n\n"
                f"ID: {pqr_id}\n"
                f"Una vez recibamos la información, te indicamos el procedimiento RMA y tiempos estimados.\n"
                f"Contacto: {support_email}"
            )
            return short_text, pqr_id, False, categoria or "Garantías"
    except Exception:
        pass

    # Escalamiento por palabras clave, además del flag del modelo
    lower_msg = (message or "").lower()
    if any(t in lower_msg for t in ESCALAMIENTO):
        requires_human = True

    email_contact = os.getenv("YAMAKI_CONTACT_EMAIL", CANALES_ATENCION_YAMAKI.get("email"))
    support_email = os.getenv("YAMAKI_SUPPORT_EMAIL", CANALES_ATENCION_YAMAKI.get("soporte"))
    whatsapp = os.getenv("YAMAKI_WHATSAPP", CANALES_ATENCION_YAMAKI.get("whatsapp"))

    if requires_human:
        text = (
            f"Gracias por tu mensaje. Hemos escalado tu consulta a un asesor humano.\n\n"
            f"ID: {pqr_id}\n"
            f"Te contactaremos pronto. Si deseas, escribe a {email_contact} o {support_email}.\n"
            f"WhatsApp: {whatsapp}"
        )
        return text, pqr_id, True, categoria or "General"

    # Respuesta breve y profesional
    pqr_prompt = f"""
Como asesor de Yamaki, redacta una respuesta breve (≤150 palabras) y empática para el cliente.

ID: {pqr_id}
Tipo: {tipo_pqr}
Categoría: {categoria}
Marca: {marca}
Asunto: {asunto}
Descripción: "{descripcion}"

Instrucciones:
- Confirma recepción con el ID.
- Incluye próximos pasos y tiempos aproximados.
- Si aplica, sugiere compartir marca, modelo, cantidad y ciudad.
- Menciona que puede contactar soporte en {support_email}.
- Cierra como Yamaki.

Respuesta:
"""

    completion = client.chat.completions.create(
        model="UnosquareGPT4oModel",
        messages=[{"role": "user", "content": pqr_prompt}],
    )
    response_text = completion.choices[0].message.content

    # Resumen si es demasiado larga
    if len(response_text) > 450:
        summary_prompt = f"""
Resume a ≤150 palabras manteniendo ID {pqr_id}, próximos pasos y contacto {support_email}.
Texto original: "{response_text}"
"""
        summary_completion = client.chat.completions.create(
            model="UnosquareGPT4oModel",
            messages=[{"role": "user", "content": summary_prompt}],
        )
        response_text = summary_completion.choices[0].message.content

    return response_text, pqr_id, False, categoria or "General"


