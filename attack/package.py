import time
import numpy as np
import pandas as pd
import stix2

from config import Config
from embeddings import get_embeddings
from stix2 import FileSystemSource, CompositeDataSource, Filter


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

    filter_list: list[stix2.Filter] = Filter("type", "=", "attack-pattern")

    return src.query(filter_list)


def format_data():
    """
    Extract id, name, description of the technique and get its embeddings depends on description.
    """
    techniques: list = get_data()

    length: int = len(techniques)

    format_list: list = []
    GREEN: str = '\033[32m'
    RESET: str = '\033[0m'
    # LOADING_SYMBOLS: list = ['|', '/', '-', '\\']
    for technique in techniques:
        for i in range(length):
            print('\r', end='')
            print(f'{GREEN}In Process: {technique["external_references"][0]["external_id"]} --- {technique["name"]}... '
                  f'[{i+1}/{length}]{RESET}\n', end='', flush=True)
            time.sleep(1)

            # deprecated items
            if 'x_mitre_deprecated' in technique and technique['x_mitre_deprecated'] is True:
                continue

            description: str = ''
            embedding: np.ndarray = np.zeros(None)
            if 'description' in technique:
                description = technique["description"]
                get_embeddings(description)  # get embeddings depends on description

            format_dict: dict[str, str] = {
                "id": technique["external_references"][0]["external_id"],
                "name": technique["name"],
                "description": description,
                "embedding": embedding
            }

            format_list.append(format_dict)

        # show all columns
        pd.set_option('display.max_columns', None)
        pd.set_option('expand_frame_repr', False)

        df: pd.DataFrame = pd.DataFrame(format_list)
        df.to_csv('mitre_att&ck.csv')
