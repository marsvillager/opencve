import os


class Config:
    """
    Variables.
    """
    BASE_DIR: str = os.path.dirname(os.path.dirname(__file__))

    URL: str = "https://github.com/mitre/cti.git"

    MITRE_ATTACK_DATA_PATH: str = BASE_DIR + "/attack/data/"