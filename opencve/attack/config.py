RED: str = '\033[31m'
GREEN: str = '\033[32m'
BLUE: str = '\033[34m'
RESET: str = '\033[0m'

CTI_URL: str = "https://github.com/mitre/cti.git"

PROXY = {
        'http': 'http://127.0.0.1:1087',
        'https': 'http://127.0.0.1:1087'
}

# configuration of attack
MITRE_ATTACK_LOG_PATH: str = "./log/"
MITRE_ATTACK_DATA_PATH: str = "./data/"
CHECKPOINT_FILE: str = './checkpoint.txt'
EMBEDDINGS_FILE: str = './embeddings/'

# 分批处理
BATCH: int = 20000

# Display top [RANK]
RANK: int = 5
