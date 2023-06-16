import os
import configparser
from pathlib import Path, PosixPath

PROXY = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
}

WORK_DIRECTORY: PosixPath = Path(__file__).parent.resolve()
DEFAULT_CONFIG: PosixPath = Path(__file__).parent.resolve() / "default.cfg"
DEFAULT_WELCOME_FILES: PosixPath = Path(__file__).parent.resolve() / "templates/_welcome"
OPENCVE_HOME: str = os.environ.get("OPENCVE_HOME") or str(Path.home() / "opencve")
OPENCVE_CONFIG: str = os.environ.get("OPENCVE_CONFIG") or str(
    Path(OPENCVE_HOME) / "opencve.cfg"
)
OPENCVE_WELCOME_FILES: str = os.environ.get("OPENCVE_WELCOME_FILES") or str(
    Path(OPENCVE_HOME) / "welcome_html"
)

# WORK_DIRECTORY: str = os.path.dirname(os.path.dirname(__file__))
# DEFAULT_CONFIG: str = WORK_DIRECTORY + '/opencve/default.cfg'
# DEFAULT_WELCOME_FILES: str = WORK_DIRECTORY + '/opencve/templates/_welcome'
# OPENCVE_HOME: str = os.environ.get("OPENCVE_HOME") or WORK_DIRECTORY + '/opencve'
# OPENCVE_CONFIG: str = os.environ.get("OPENCVE_CONFIG") or WORK_DIRECTORY + '/conf/opencve.cfg'
# OPENCVE_WELCOME_FILES = os.environ.get("OPENCVE_WELCOME_FILES") or WORK_DIRECTORY + "/conf/welcome_html"

# Load the configuration
config = configparser.ConfigParser()

if Path(OPENCVE_CONFIG).exists():
    config.read(OPENCVE_CONFIG)
else:
    config.read(DEFAULT_CONFIG)

    # Generate a secret to avoid the following warning when init the config :
    # WARNING: Flask-User TokenManager: SECRET_KEY is shorter than 32 bytes.
    config.set("core", "secret_key", " " * 32)

# configuration of attack
MITRE_ATTACK_LOG_PATH: str = OPENCVE_HOME + "/log/"
MITRE_ATTACK_DATA_PATH: PosixPath = WORK_DIRECTORY / "attack/data/"
CHECKPOINT_FILE: PosixPath = WORK_DIRECTORY / 'attack/checkpoint.txt'
EMBEDDINGS_FILE: PosixPath = WORK_DIRECTORY / 'attack/embeddings/'

# 分批处理
BATCH: int = 20000

# Display top [RANK]
RANK: int = 5
