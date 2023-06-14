import configparser
import os

from pathlib import Path


class Config:
    """
    Variables.
    """
    BASE_DIR: str = os.path.dirname(os.path.dirname(__file__))

    CTI_URL: str = "https://github.com/mitre/cti.git"

    MITRE_ATTACK_DATA_PATH: str = BASE_DIR + "/attack/data/"

    PROXY = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }

    # OpenAI URL
    EMBEDDINGS_URL = 'https://api.openai.com/v1/embeddings'

    # ChatGPT API, located in opencve.cfg(created after `opencve init`)
    OPENCVE_HOME = os.environ.get("OPENCVE_HOME")  # 注意路径问题，设置的是相对路径，一般是 ./conf，但目的是在 root/opencve下创建conf
    OPENCVE_CONFIG = str(BASE_DIR / Path(OPENCVE_HOME) / "opencve.cfg")  # 转绝对路径

    opencve_config = configparser.ConfigParser()
    if Path(OPENCVE_CONFIG).exists():
        opencve_config.read(OPENCVE_CONFIG)

    CHATGPT_API = opencve_config.get("core", "chatgpt_api")