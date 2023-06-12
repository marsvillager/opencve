import requests


url = 'https://api.openai.com/v1/chat/completions'
proxy = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}


# def request_prompt(app, prompt):
prompt = "say this is a test"
openai_api_key = ""
    # openai_api_key = app.config["CHATGPT_API"]

headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}',
    }   

data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }

response = requests.post(url, headers=headers, json=data, proxies=proxy)

    # return response.json()
