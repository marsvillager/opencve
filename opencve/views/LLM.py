# import openai

# openai.api_key = ""
# openai.api_base = "https://api.chatanywhere.com.cn/v1"


# def opencve_chat(opencve_info,machine_info):
#     prompt=[
#         # {
#         #     "role": "system",
#         #     "content": '''
#         #     你是一个cve检测系统,我将依次给你一个json格式cve信息和一个json格式终端信息,仔细分析cve影响的系统与版本范围,
#         #     请将cve信息中受影响的系统型号系列与版本范围信息按条理解整理.
#         #     '''
#         # },
#         # {
#         #     "role": "user",
#         #     "content": "cve信息如下:"+opencve_info
#         # },
#         # {
#         #     "role": "user",
#         #     "content": "主机信息如下:"+machine_info
#         # },
#         # {
#         #     "role":"user",
#         #     "content":'''
#         #     请将上述终端信息与此cve信息进行匹配,在进行匹配时有先后关系,终端的型号是否属于此cve的影响系列在先,版本号是否属于受影响的范围在后,终端信息只需要满足一个配即认为是受到影响的,
#         #     终端与版本号是相关联的,终端类型未完全匹配无需进行版本对比.
#         #     终端型号匹配时仅需要进行匹配(即系列相同或为包含关系),进行延伸推测的Possibility需要相应较低.
#         #     注意版本号比较规则,版本号的层级从左往右大版本在前,小版本在后,数字越小版本越低,比如1.1.2大于1.1.1,
#         #     终端信息中没有证据与此cve相关无法确定时,可以初步认定没有受到影响概率输出0%,最后请以(原因:,终端受到此cve影响的Possibility:)的句式进行回答.其中原因请给出详细的分析过程并给明终端类型与系列的匹配结果以及版本号比较结果,Possibility请给出终端受到此cve影响的百分比数字.
#         #     '''
#         # }
#         {
#             "role": "system",
#             "content": '''
#             ou are a CVE detection system. I will give you a CVE information in json format and a endpint information in json format in sequence, please analyze the system and version range affected by this CVE.
#             The system model series and version range information included in the submitted CVE information are organized in an organized manner.
#             '''
#             },
#         {
#             "role": "user",
#             "content": "CVE information as follows:"+opencve_info
#         },
#         {
#             "role": "user",
#             "content": "endpoint information as follows:"+machine_info
#         },
#         {
#             "role":"user",
#             "content":'''
#             The response terminal information is matched with this CVE information. There is a subsequent relationship when matching. Whether the terminal model belongs to the impact series of this CVE comes first, and whether the version number belongs to the range of hiking.Terminal information only needs to meet one configuration to be considered affected.
#             The terminal and version number are related, and the terminal type does not fully meet the consumption for version comparison.
#             The final model matching only needs to be matched (i.e. the series are identical or inclusive), and the likelihood of inference needs to be correspondingly low.
#             Pay attention to the version number comparison rules. The version number system is from left to right, with the larger version first and the smaller version last. The smaller the number, the lower the version. For example, 1.1.2 is greater than 1.1.1.
#             When there is no evidence in the terminal information related to this CVE and it cannot be determined, it can be initially determined that the probability of not being affected is 0%. Finally, please answer with the sentence pattern of (reason:, the possibility that the terminal is affected by this CVE:). Please provide a detailed analysis process for the reasons and clear answer types and series matching results and version number comparison results. Please provide the possibility affected by this CVE. Don't answer me high or low ,give me the possibilty number .
#             '''
#         }
#     ]

#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=prompt,
#         temperature=0,
#         frequency_penalty=0.0,
#         presence_penalty=-2
#     )
#     return response["choices"][0]["message"]["content"]

## zhipuai
from zhipuai import ZhipuAI
client = ZhipuAI(api_key="37cd7d8b6edc59e44d70aa9271576ba3.gzlVGucdqzBCf1tj") 

def opencve_chat(opencve_info,machine_info):

    response = client.chat.completions.create(
        model="glm-4",  
        messages=[
            {
                "role": "system",
                "content": '''
                你是一个cve检测系统,我将依次给你一个json格式cve信息和一个json格式终端信息,仔细分析此cve影响的系统与版本范围,
                请将cve信息中受影响的系统型号系列与版本范围信息按条理解整理.
                '''
                },
            {
                "role": "user",
                "content": "cve信息如下:"+opencve_info
            },
            {
                "role": "user",
                "content": "主机信息如下:"+machine_info
            },
            {
                "role":"user",
                "content":'''
                请将终端信息与此cve信息进行匹配,在进行匹配时有先后关系,终端的型号是否属于此cve的影响系列在先,版本号是否属于受影响的范围在后,终端信息只需要满足一个配置信息即可认为是受到影响的,
                终端与版本号是相关联的,终端类型未完全匹配无需进行版本对比.
                终端型号匹配时仅需要进行匹配(即系列相同或为包含关系),进行延伸推测的Possibility需要相应较低.
                注意版本号比较规则,版本号的层级从左往右大版本在前,小版本在后,数字越小版本越低,
                终端信息中没有证据与此cve相关无法确定时,可以初步认定没有受到影响概率输出0%,最后请以(原因:,终端受到此cve影响的Possibility:)的句式进行回答.其中原因请给出详细的分析过程并给明终端类型与系列的匹配结果以及版本号比较结果,Possibility请给出终端受到此cve影响的百分比数字,不要给回答高或者低,给出具体概率数值.
                '''
            }
            # {
            #     "role": "system",
            #     "content": '''
            #     ou are a CVE detection system. I will give you a CVE information in json format and a endpint information in json format in sequence, please analyze the system and version range affected by this CVE.
            #     The system model series and version range information included in the submitted CVE information are organized in an organized manner.
            #     '''
            #     },
            # {
            #     "role": "user",
            #     "content": "CVE information as follows:"+opencve_info
            # },
            # {
            #     "role": "user",
            #     "content": "endpoint information as follows:"+machine_info
            # },
            # {
            #     "role":"user",
            #     "content":'''
            #     The response terminal information is matched with this CVE information. There is a subsequent relationship when matching. Whether the terminal model belongs to the impact series of this CVE comes first, and whether the version number belongs to the range of hiking.Terminal information only needs to meet one configuration to be considered affected.
            #     The terminal and version number are related, and the terminal type does not fully meet the consumption for version comparison.
            #     The final model matching only needs to be matched (i.e. the series are identical or inclusive), and the likelihood of inference needs to be correspondingly low.
            #     Pay attention to the version number comparison rules. The version number system is from left to right, with the larger version first and the smaller version last. The smaller the number, the lower the version.
            #     When there is no evidence in the terminal information related to this CVE and it cannot be determined, it can be initially determined that the probability of not being affected is 0%. Finally, please answer with the sentence pattern of (reason:, the possibility that the terminal is affected by this CVE:). Please provide a detailed analysis process for the reasons and clear answer types and series matching results and version number comparison results. Please provide the possibility affected by this CVE.Don't answer me high or low ,give me the possibilty number .
            #     '''
            # }
        ],
    )

    return response.choices[0].message.content
