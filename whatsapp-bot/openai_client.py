from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
# Configure credentials
azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
api_key = os.getenv('AZURE_OPENAI_API_KEY')

client = AzureOpenAI(
    api_version="2023-05-15",
    azure_endpoint=azure_endpoint,
    api_key=api_key)

def gpt_connection(prompt):
    completion = client.chat.completions.create(
        model="UnosquareGPT4oModel",
        messages=[{
            "role": "user",
            "content": f"{prompt}",
        }],
    )
    return completion.choices[0].message.content

# Nota: El corte de mensajes largos se maneja en app.py