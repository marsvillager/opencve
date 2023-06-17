import glob
import pickle
import requests
import numpy as np

from opencve.configuration import EMBEDDINGS_FILE, RANK, config
from opencve.commands import info

# OpenAI URL
EMBEDDINGS_URL: str = 'https://api.openai.com/v1/embeddings'

# OpenAI API key
OPENAI_API_KEY: str = config.get("core", "openai_api_key")

# proxy
PROXY: list = {
    'http': config.get("core", "http_proxy"),
    'https': config.get("core", "https_proxy"),
}


def get_embeddings(input):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}',
    }

    data = {
        "model": "text-embedding-ada-002",
        "input": input
    }

    info(PROXY)

    response = requests.post(EMBEDDINGS_URL, headers=headers, json=data, proxies=PROXY)

    # dict_keys(['object', 'data', 'model', 'usage'])
    vect_list: list = response.json()["data"][0]["embedding"]

    return np.array(vect_list)


def calc_distance(input):
    src_vector: np.array = get_embeddings(input)

    # 整合分批处理后的所有.pkl文件
    id_file: str = str(EMBEDDINGS_FILE / '*.pkl')
    format_dict: dict[tuple, np.array] = {}
    for file in glob.glob(id_file):
        with open(file, 'rb') as f:
            format_dict.update(pickle.load(f))

    for item in format_dict.keys():
        # 距离度量方法
        # format_dict[item] = np.sqrt(np.sum(np.square(format_dict[item] - src_vector)))

        # return sorted(format_dict.items(), key=lambda k: float(k[1]), reverse=False)[:RANK]
        
        # 相似度度量方法
        format_dict[item] = np.dot(format_dict[item], src_vector) / (
                    np.linalg.norm(format_dict[item]) * np.linalg.norm(src_vector))

    return sorted(format_dict.items(), key=lambda k: float(k[1]), reverse=True)[:RANK]  
