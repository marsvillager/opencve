import pandas as pd
from get_embeddings import get_embeddings
import stix2

from config import Config
from stix2 import FileSystemSource, CompositeDataSource, Filter


def get_data() -> list:
    """
    Extract data depends on stix2.

    :param filter_list: filter by classification
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


def format_data() -> pd.DataFrame:
    """
    Extract technique data which is key to process then match.

    :param lemma: word ==> lemma if True, stay the same if False
    :return: formatted data
    """
    techniques: list = get_data()

    format_list: list = []
    for technique in techniques:
        # deprecated items
        if 'x_mitre_deprecated' in technique and technique['x_mitre_deprecated'] is True:
            continue

        description: str = ''
        # embedding: = ''
        if 'description' in technique:
            description = technique["description"]
            # get_embeddings(description)


        format_dict: dict[str, str] = {
            "id": technique["external_references"][0]["external_id"],
            "name": technique["name"],
            "description": description
            # "embedding": 
        }

        format_list.append(format_dict)
        

    # show all columns
    pd.set_option('display.max_columns', None)
    pd.set_option('expand_frame_repr', False)

    df: pd.DataFrame = pd.DataFrame(format_list)
    df.to_csv('mitre_att&ck.csv')
