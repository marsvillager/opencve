import os.path
import numpy as np
import stix2

from stix2 import FileSystemSource, CompositeDataSource, Filter
from opencve.attack.calculation import get_embeddings
from opencve.constants import GREEN, RESET
from opencve.configuration import MITRE_ATTACK_DATA_PATH, CHECKPOINT_FILE, BATCH


def get_data() -> list:
    """
    Extract data depends on stix2.

    :return: techniques of stix2
    """
    enterprise_attack_src: stix2.FileSystemSource = FileSystemSource(str(MITRE_ATTACK_DATA_PATH / "enterprise-attack"))
    mobile_attack_src: stix2.FileSystemSource = FileSystemSource(str(MITRE_ATTACK_DATA_PATH / "mobile-attack"))
    ics_attack_src: stix2.FileSystemSource = FileSystemSource(str(MITRE_ATTACK_DATA_PATH / "ics-attack"))

    src = CompositeDataSource()
    src.add_data_sources([enterprise_attack_src, mobile_attack_src, ics_attack_src])

    filter_list: list[stix2.Filter] = Filter("type", "=", "attack-pattern")

    return src.query(filter_list)


def save_checkpoint(checkpoint: int):
    with open(CHECKPOINT_FILE, 'w') as file:
        file.write(str(checkpoint))


def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r') as file:
            return int(file.read())
    return 0


def format_data(format_dict, count) -> bool:
    """
    Extract id, name, description of the technique and get its embeddings depends on description.
    
    :param format_dict: dict[tuple, np.array]
    :param count: 分批处理
    :return: end or not
    """
    techniques: list = get_data()

    length: int = len(techniques)

    checkpoint: int = load_checkpoint()

    if checkpoint >= length:
        print("Congratulations! Task completed 🎉🎉🎉")
        return True

    for technique in techniques[checkpoint:]:
        # 注意终止条件，如果内部不限制可能会绕过分批处理的设计
        if checkpoint >= BATCH * count:
            return False

        print('\r', end='')
        print(f'{GREEN}In Process: [{checkpoint+1}/{length}]  {technique["external_references"][0]["external_id"]} --- '
              f'{technique["name"]}{RESET}\n', end='', flush=True)

        # deprecated items
        if 'x_mitre_deprecated' in technique and technique['x_mitre_deprecated'] is True:
            continue

        # 没有描述无法匹配
        if 'description' not in technique:
            continue

        embedding: np.array = get_embeddings(technique["description"])  # get embeddings depends on description

        # get_embeddings 这一步由于网络的不稳定极可能结束进程，而要处理的数据有很庞大，因此需要保存断点
        checkpoint += 1
        save_checkpoint(checkpoint)

        # save dict in list
        format_dict[tuple([technique["external_references"][0]["external_id"], technique["name"]])] = embedding

    return False
