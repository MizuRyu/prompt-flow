import os
from openai import AzureOpenAI
from promptflow.tracing import start_trace

from dotenv import load_dotenv

load_dotenv()

api_endpoint = os.getenv("AOAI_BASE")
api_key = os.getenv("AOAI_KEY")
api_version = os.getenv("AOAI_VERSION")

client = AzureOpenAI(
    azure_endpoint=api_endpoint,
    api_key=api_key,
    api_version=api_version
)

start_trace(collection="trace-openai-helloworld")

system_prompt = "あなたはAIアシスタントです。"
user_prompt = "東京について教えて"

response = client.chat.completions.create(
    model="gpt-35-turbo-1106",
    temperature=0.7,
    max_tokens=500,
    
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
)

print(response.choices[0].message.content)
