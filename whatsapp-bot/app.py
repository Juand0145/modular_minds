from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
from openai_client import gpt_connection

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
    incoming_msg = request.values.get('Body', '').lower()
    sender = request.values.get('From')

    print(sender)
    print("-" * 100)
    print(incoming_msg)
    print("-" * 100)

    bot_response = gpt_connection(incoming_msg)
    
    # Split the response into chunks of max 1000 characters
    MAX_LENGTH = 1000
    response = MessagingResponse()
    for i in range(0, len(bot_response), MAX_LENGTH):
        part = bot_response[i:i+MAX_LENGTH]
        response.message(part)
    print(str(response)) 
    
    return str(response)

if __name__ == '__main__':
    app.run(port=5000)