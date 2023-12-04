



import openai


openai.api_key = "sk-0A10ygddkOtZoeMUiVBHaOozf1eW2yA5wu3llgyAkbGAesen"
openai.api_base = "https://api.chatanywhere.com.cn/v1"

def opencve_chat(opencve_info,machine_info):
    prompt=[
        {
            "role": "system",
            "content": "我将依次给你一个json格式cve的相关配置信息和json格式的主机相关信息,请根据cve中的配置信息后对比主机相关信息，给出主机受到此cve影响的概率（0到100）."
        },
        {
            "role": "user",
            "content": opencve_info
        },
        {
            "role": "user",
            "content": machine_info
        }

    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=0,
        # max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    print(response["choices"][0]["message"]["content"])
    return response["choices"][0]["message"]["content"]
