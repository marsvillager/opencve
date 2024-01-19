import openai

openai.api_key = "sk-ZDhO81XNnGIohah4WQaTP8fAs35hNCJQNP56eKNAKUUMRY6S"
openai.api_base = "https://api.chatanywhere.tech/v1"


def opencve_chat(opencve_info,machine_info):
    prompt=[
        {
            "role": "system",
            "content": "你是一个cve检测系统，我将依次给你一个json格式cve信息和一个json格式主机信息,请通过语义匹配能力得到主机受到cve影响的概率（请注意版本号的比较规则）,请分别给出原因和概率，其中原因请给出详细的分析过程并附带主机的相关信息，概率给出主机受到此cve影响的百分比数字.(回答不要使用单引号:')"
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
        frequency_penalty=0.0,
        presence_penalty=0.0
    )


    return response["choices"][0]["message"]["content"]
