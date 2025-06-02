from openai import AzureOpenAI

client = AzureOpenAI(
    api_version="2023-05-15",
    azure_endpoint="https://gabirelunosquareopenai.openai.azure.com/",
    api_key="799e57477164420a81e76bc1fa05330d")

def gpt_connection(prompt):
    completion = client.chat.completions.create(
        model="UnosquareGPT4oModel",
        messages=[{
            "role": "user",
            "content": f"{prompt}",
        }],
    )
    return completion.choices[0].message.content