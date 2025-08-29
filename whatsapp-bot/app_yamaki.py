from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
import json

from yamaki_openai import classify_yamaki, generate_response_yamaki
from yamaki_faq import answer_faq_or_none
from yamaki_config import ESCALAMIENTO, CANALES_ATENCION_YAMAKI, MARCAS
from yamaki_escalation import notify_human_escalation


load_dotenv()

# Twilio
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

app = Flask(__name__)

DEMO_MODE = os.getenv("DEMO_MODE", "1") == "1" or not os.getenv("DATABASE_URL")

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    incoming_msg = request.values.get("Body", "")
    sender = request.values.get("From")

    print("-" * 50)
    print(f"Usuario: {sender}")
    print(f"Mensaje: {incoming_msg}")

    # Inicializar DB (idempotente) solo si NO es demo
    if not DEMO_MODE:
        try:
            from yamaki_db import init_db  # Import diferido para evitar dependencia en demo
            init_db()
        except Exception as e:
            print(f"[DB] init_db omitido (demo o error): {e}")

    # Intento de respuesta por FAQ rápida
    faq_answer = answer_faq_or_none(incoming_msg)

    # Clasificación por IA
    classification_data = classify_yamaki(incoming_msg) or "{}"
    clean_classification = classification_data
    try:
        if "```" in clean_classification:
            if "```json" in clean_classification:
                clean_classification = clean_classification.split("```json")[1].split("```")[0].strip()
            else:
                clean_classification = clean_classification.split("```")[1].strip()
        parsed = json.loads(clean_classification)
    except Exception as e:
        print(f"Error parseando clasificación en app: {e}")
        parsed = {}

    lower_msg = incoming_msg.lower()
    # Solo escalar por disparadores explícitos, ignorar bandera del modelo
    requires_human = any(t in lower_msg for t in ESCALAMIENTO)

    # Generar respuesta base
    bot_response, pqr_id, requires_human_model, categoria = generate_response_yamaki(
        sender, incoming_msg, classification_data
    )
    # No combinar con la bandera del modelo; mantener solo disparadores explícitos

    # Si hay FAQ y no requiere humano, usarla SOLO si no hay marca detectada
    if faq_answer and not requires_human and pqr_id != "BIENVENIDA":
        brands_lower = [b.lower() for b in MARCAS]
        detected_brand = str(parsed.get("marca", "")).lower()
        has_brand_detected = bool(detected_brand) and detected_brand != "otra"
        msg_has_brand = any(b in lower_msg for b in brands_lower)
        if not (has_brand_detected or msg_has_brand):
            bot_response = (
                f"{faq_answer}\n\n"
                f"Si necesitas más ayuda o una cotización, indícanos marca, modelo y ciudad."
            )

    # Enviar respuesta en fragmentos
    MAX_LENGTH = 800
    response = MessagingResponse()
    for i in range(0, len(bot_response), MAX_LENGTH):
        part = bot_response[i : i + MAX_LENGTH]
        response.message(part)

    # Construir payload técnico para logs internos (no se envía al usuario)
    try:
        payload = {
            "id": pqr_id,
            "usuario": sender,
            "mensaje": incoming_msg,
            "clasificacion": parsed,
            "categoria": categoria,
            "requires_human": requires_human,
            "demo": DEMO_MODE,
        }
        print("📊 Payload técnico:", json.dumps(payload, ensure_ascii=False))
    except Exception:
        print("📊 Payload técnico no disponible")

    # Persistencia (si hay DB)
    if not DEMO_MODE:
        try:
            from yamaki_db import save_interaction  # Import diferido para evitar dependencia en demo
            save_interaction(
                user_phone=sender or "",
                category=categoria or parsed.get("categoria") or "General",
                subject=parsed.get("asunto", "Consulta"),
                description=parsed.get("descripcion") or incoming_msg,
                subcategory=parsed.get("subcategoria"),
                brand=parsed.get("marca"),
                model=None,
                city=None,
                classification_data=parsed or None,
                response_text=bot_response,
                pqr_id=pqr_id if pqr_id != "BIENVENIDA" else f"TEMP-{sender[-4:]}",
                pqr_type=parsed.get("tipo_pqr", "Solicitud"),
                requires_human=requires_human,
            )
        except Exception as e:
            print(f"[DB] No se pudo guardar interacción: {e}")

    # Notificación de escalamiento (opcional, según SMTP y email configurados)
    if requires_human:
        try:
            result = notify_human_escalation(payload)
            if result:
                print(result)
        except Exception as e:
            print(f"[Escalation] Error notificando: {e}")

    return str(response)


if __name__ == "__main__":
    app.run(port=5000)


