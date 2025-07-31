from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime

load_dotenv()
# Configure credentials
azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
api_key = os.getenv('AZURE_OPENAI_API_KEY')

client = AzureOpenAI(
    api_version="2023-05-15",
    azure_endpoint=azure_endpoint,
    api_key=api_key)

def classify_pqr(message):
    """Clasifica el mensaje del usuario para identificar tipo de PQR y categorías."""
    classification_prompt = f"""
    Clasifica este mensaje de cliente de Erco Energía (empresa de energía solar):

    "{message}"

    Responde SOLO en formato JSON:
    {{
        "tipo_pqr": "Saludo/Queja/Petición/Solicitud",
        "asunto": "Resumen en 5 palabras",
        "categoria": "Bienvenida/Facturación/Servicio técnico/Atención al cliente/Energía Solar",
        "descripcion": "Problema resumido en 15 palabras máximo"
    }}
    
    EJEMPLOS de SALUDOS que deben ser categoria "Bienvenida":
    - "Hola", "Hi", "Hello", "Buenos días"
    - "Buenas tardes", "Buenas noches", "Buenas"
    - "Me presento", "Necesito ayuda", "Ayuda"
    - "Qué tal", "Saludos", "Inicio"
    - "Empiezo", "Empezar", "Me pueden ayudar"
    - "Tengo una consulta", "Información por favor"
    
    EJEMPLOS de "Energía Solar":
    - "Quiero paneles solares", "Cotización energía solar"
    - "Instalación residencial", "Ampliación sistema"
    - "Movilidad eléctrica", "Baterías almacenamiento"
    """
    
    try:
        completion = client.chat.completions.create(
            model="UnosquareGPT4oModel",
            messages=[{
                "role": "user",
                "content": classification_prompt,
            }],
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error en clasificación: {e}")
        return None

def generate_pqr_response(user_phone, message, classification_data):
    """Genera una respuesta profesional para PQR usando el prompt personalizado."""
    
    # Generar ID único para la PQR
    pqr_id = f"PQR-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
    
    # Extraer nombre del número de teléfono (simplificado)
    user_name = f"Usuario {user_phone[-4:]}"
    
    try:
        # Parsear datos de clasificación (limpiando formato markdown)
        import json
        if classification_data:
            try:
                # Limpiar el JSON si viene en formato markdown
                clean_json = classification_data
                if "```json" in clean_json:
                    clean_json = clean_json.split("```json")[1].split("```")[0].strip()
                elif "```" in clean_json:
                    clean_json = clean_json.split("```")[1].strip()
                
                print(f"Información PQR: {clean_json}")  # Debug
                
                class_data = json.loads(clean_json)
                tipo_pqr = class_data.get('tipo_pqr', 'Solicitud')
                asunto = class_data.get('asunto', 'Consulta general')
                categoria = class_data.get('categoria', 'Atención al cliente')
                descripcion = class_data.get('descripcion', message)
                
                print(f"Categoria detectada: {categoria}, Tipo: {tipo_pqr}")  # Debug
                
            except Exception as parse_error:
                print(f"Error parseando JSON: {parse_error}")
                # Si falla el parsing, revisar si es saludo manualmente
                if any(word in message.lower() for word in ['hola', 'buenos días', 'buenas tardes', 'buenas noches', 'hi', 'hello', 'saludos']):
                    tipo_pqr = 'Saludo'
                    asunto = 'Saludo inicial'
                    categoria = 'Bienvenida'
                    descripcion = message
                    print("🔧 DETECCIÓN MANUAL DE SALUDO ACTIVADA")
                else:
                    # Si falla el parsing, usar valores por defecto
                    tipo_pqr = 'Solicitud'
                    asunto = 'Consulta general'
                    categoria = 'Atención al cliente'
                    descripcion = message
        else:
            tipo_pqr = 'Solicitud'
            asunto = 'Consulta general'
            categoria = 'Atención al cliente'
            descripcion = message
            
    except Exception as e:
        print(f"Error procesando clasificación: {e}")
        tipo_pqr = 'Solicitud'
        asunto = 'Consulta general'
        categoria = 'Atención al cliente'
        descripcion = message

    # Si es un saludo/bienvenida, devolver mensaje de bienvenida directamente
    print(f"Verificando bienvenida - Categoria: '{categoria}', Tipo: '{tipo_pqr}'")  # Debug
    
    if (categoria and categoria.lower() == 'bienvenida') or (tipo_pqr and tipo_pqr.lower() == 'saludo'):
        print("🎉 DETECTADO COMO BIENVENIDA - Enviando mensaje de bienvenida")  # Debug
        welcome_response = """¡Hola! Soy *Ercobot*, el asistente virtual Demo de Erco Energía ☀️

Puedo ayudarte con:
• Energía Solar 🌞
• Facturación ⚡
• Servicio técnico 🔧
• Atención al cliente 📋
• Monitoreo ENRG 📱

¿En qué te puedo ayudar hoy?"""
        return welcome_response, "BIENVENIDA"

    pqr_prompt = f"""
    Como Ercobot, asistente virtual oficial de Erco Energía S.A.S., genera una respuesta BREVE y empática para la siguiente {tipo_pqr}:

    ID: {pqr_id}
    Asunto: {asunto}
    Descripción: "{descripcion}"
    
    REQUISITOS (máximo 150 palabras):
    - Saludo cordial mencionando a Erco Energía
    - Confirmar recepción con ID único
    - Explicar proceso de seguimiento
    - Tiempo estimado de respuesta: 5 días hábiles máximo
    - Mencionar app ENRG para seguimiento
    - Contacto: WhatsApp +57 601 6659652 opción 3
    - Despedida profesional firmada como Ercobot
    
    Respuesta concisa:
    """
    
    completion = client.chat.completions.create(
        model="UnosquareGPT4oModel",
        messages=[{
            "role": "user",
            "content": pqr_prompt,
        }],
    )
    
    response_text = completion.choices[0].message.content
    
    # Post-procesamiento para garantizar brevedad
    if len(response_text) > 400:  # Si es muy larga, resumir
        summary_prompt = f"""
        Resume esta respuesta a máximo 150 palabras manteniendo:
        - ID: {pqr_id}
        - Información esencial
        - Contacto: WhatsApp +57 601 6659652 opción 3
        - App ENRG para seguimiento
        - Firma: Ercobot, Erco Energía
        
        Texto original: "{response_text}"
        
        Resumen conciso:
        """
        
        summary_completion = client.chat.completions.create(
            model="UnosquareGPT4oModel",
            messages=[{"role": "user", "content": summary_prompt}],
        )
        response_text = summary_completion.choices[0].message.content
    
    return response_text, pqr_id

def gpt_connection(prompt):
    """Función legacy para compatibilidad - ahora redirige a PQR."""
    completion = client.chat.completions.create(
        model="UnosquareGPT4oModel",
        messages=[{
            "role": "user",
            "content": f"{prompt}",
        }],
    )
    return completion.choices[0].message.content

# Nota: El corte de mensajes largos se maneja en app.py