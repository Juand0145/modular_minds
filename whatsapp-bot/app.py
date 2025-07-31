from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
from openai_client import classify_pqr, generate_pqr_response, gpt_connection
from pqr_config import EMERGENCIAS, RESPUESTA_EMERGENCIA

# Load environment variables
load_dotenv()

# Configure credentials
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

app = Flask(__name__)

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    # Get the user's message
    incoming_msg = request.values.get('Body', '')
    sender = request.values.get('From')

    print("-" * 50)
    print(f"Usuario: {sender}")
    print(f"Mensaje: {incoming_msg}")
    
    # Inicializar variables por defecto
    classification_data = "{}"
    pqr_id = "DESCONOCIDO"
    bot_response = "Error en el procesamiento del mensaje."
    
    # Detectar emergencias primero (para casos críticos)
    mensaje_lower = incoming_msg.lower()
    es_emergencia = any(palabra in mensaje_lower for palabra in EMERGENCIAS)
    
    try:
        if es_emergencia:
            bot_response = RESPUESTA_EMERGENCIA
            pqr_id = f"EMERGENCIA-{incoming_msg[:20].replace(' ', '')}"
            classification_data = classify_pqr(incoming_msg)
            print(f"🚨 EMERGENCIA DETECTADA: {pqr_id}")
        else:
            # Clasificar TODA consulta (incluyendo saludos) usando IA
            classification_data = classify_pqr(incoming_msg)
            # print(f"Clasificación: {classification_data}")
            
            # Generar respuesta usando el sistema PQR inteligente
            bot_response, pqr_id = generate_pqr_response(sender, incoming_msg, classification_data)
    except Exception as e:
        print(f"Error al procesar mensaje: {str(e)}")
        bot_response = "Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta nuevamente."
        pqr_id = "ERROR"
        classification_data = f'{{"error": "{str(e)}", "tipo_pqr": "error", "categoria": "sistema"}}'
        
    print(f"PQR ID: {pqr_id}")
    print(f"Respuesta del bot: {bot_response}")
    print("-" * 50)
    
    # Split the response into chunks of max 800 characters (más conciso)
    MAX_LENGTH = 800
    response = MessagingResponse()
    for i in range(0, len(bot_response), MAX_LENGTH):
        part = bot_response[i:i+MAX_LENGTH]
        response.message(part)
    
    # Si NO es un saludo, enviar payload técnico como segundo mensaje
    if pqr_id != "BIENVENIDA":
        import json
        try:
            # Limpiar JSON si viene en formato markdown
            clean_classification = classification_data
            if "```json" in clean_classification:
                clean_classification = clean_classification.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_classification:
                clean_classification = clean_classification.split("```")[1].strip()
            
            # Parse para formatear mejor
            parsed_data = json.loads(clean_classification)
            
            payload_message = f"""📊 INFORMACIÓN TÉCNICA DEL SISTEMA PQR

ID Único: {pqr_id}
Usuario: {sender}
Mensaje Original: "{incoming_msg}"

CLASIFICACION:
• Tipo: {parsed_data.get('tipo_pqr', 'N/A')}
• Asunto: {parsed_data.get('asunto', 'N/A')}
• Categoría: {parsed_data.get('categoria', 'N/A')}
• Descripción: {parsed_data.get('descripcion', 'N/A')}

⚙️ Erco Energía - Sistema PQR Ercobot v1.0"""
            
        except:
            # Si falla el parsing, mostrar datos básicos
            payload_message = f"""INFORMACIÓN TÉCNICA DEL SISTEMA PQR

🆔 ID Único: {pqr_id}
📱 Usuario: {sender}
📝 Mensaje: "{incoming_msg}"

🤖 Clasificación: {classification_data}

⚙️ Erco Energía - Sistema PQR Ercobot v1.0"""
        
        # Dividir payload si es muy largo
        # for i in range(0, len(payload_message), MAX_LENGTH):
        #     payload_part = payload_message[i:i+MAX_LENGTH]
        #     response.message(payload_part)
        
        print("📊 Payload técnico enviado")
    
    return str(response)

if __name__ == '__main__':
    app.run(port=5000)