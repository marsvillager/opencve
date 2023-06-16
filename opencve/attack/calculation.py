import glob
import pickle
import numpy as np

from opencve.attack.embeddings import get_embeddings
from opencve.attack.config import Config


def calc_distance(input):
    src_vector: np.array = get_embeddings(input)

    # 整合分批处理后的所有.pkl文件
    id_file: str = Config.EMBEDDINGS_FILE + '*.pkl'
    format_dict: dict[tuple, np.array] = {}
    for file in glob.glob(id_file):
        with open(file, 'rb') as f:
            format_dict.update(pickle.load(f))

    for item in format_dict.keys():
        format_dict[item] = np.sqrt(np.sum(np.square(format_dict[item] - src_vector)))

    return sorted(format_dict.items(), key=lambda k: float(k[1]), reverse=False)[:Config.RANK]
