import requests

from config import Config


def get_embeddings(input):
    openai_api_key = Config.CHATGPT_API

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}',
    }   

    data = {
        "model": "text-embedding-ada-002",
        "input": input
    }

    response = requests.post(Config.EMBEDDINGS_URL, headers=headers, json=data, proxies=Config.PROXY)

    return response.json()
