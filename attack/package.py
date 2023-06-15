import os.path
import numpy as np
import stix2

from stix2 import FileSystemSource, CompositeDataSource, Filter
from typing import Dict, List
from config import Config
from embeddings import get_embeddings


def get_data() -> list:
    """
    Extract data depends on stix2.

    :return: techniques of stix2
    """
    enterprise_attack_src: stix2.FileSystemSource = FileSystemSource(Config.MITRE_ATTACK_DATA_PATH +
                                                                     "enterprise-attack")
    mobile_attack_src: stix2.FileSystemSource = FileSystemSource(Config.MITRE_ATTACK_DATA_PATH + "mobile-attack")
    ics_attack_src: stix2.FileSystemSource = FileSystemSource(Config.MITRE_ATTACK_DATA_PATH + "ics-attack")

    src = CompositeDataSource()
    src.add_data_sources([enterprise_attack_src, mobile_attack_src, ics_attack_src])

    filter_list: List[stix2.Filter] = Filter("type", "=", "attack-pattern")

    return src.query(filter_list)


def save_checkpoint(checkpoint: int):
    with open(Config.CHECKPOINT_FILE, 'w') as file:
        file.write(str(checkpoint))


def load_checkpoint():
    if os.path.exists(Config.CHECKPOINT_FILE):
        with open(Config.CHECKPOINT_FILE, 'r') as file:
            return int(file.read())
    return 0


def format_data(format_list: list, count: int) -> bool:
    """
    Extract id, name, description of the technique and get its embeddings depends on description.
    """
    techniques: list = get_data()

    length: int = len(techniques)

    checkpoint: int = load_checkpoint()
    for technique in techniques[checkpoint:]:
        if checkpoint >= length:
            return True

        # 注意终止条件，如果内部不限制可能会绕过分批处理的设计
        if checkpoint >= Config.BATCH * count:
            return False

        print('\r', end='')
        print(f'{Config.GREEN}In Process: [{checkpoint+1}/{length}]  {technique["external_references"][0]["external_id"]} --- '
              f'{technique["name"]}{Config.RESET}\n', end='', flush=True)

        # deprecated items
        if 'x_mitre_deprecated' in technique and technique['x_mitre_deprecated'] is True:
            continue

        embedding: np.ndarray = np.zeros(None)
        if 'description' in technique:
            embedding = get_embeddings(technique["description"])  # get embeddings depends on description

        # get_embeddings 这一步由于网络的不稳定极可能结束进程，而要处理的数据有很庞大，因此需要保存断点
        checkpoint += 1
        save_checkpoint(checkpoint)

        format_dict: Dict[str, str] = {
            "id": technique["external_references"][0]["external_id"],
            "name": technique["name"],
            "embedding": embedding
        }

        # save dict in list
        format_list.append(format_dict)

    return False
