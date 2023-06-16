import os.path
import pickle
import sys
import numpy as np

from opencve.attack import Logger, update
from opencve.attack.process import format_data, load_checkpoint
from opencve.attack.calculation import calc_distance
from opencve.constants import RED, BLUE, RESET
from opencve.configuration import MITRE_ATTACK_LOG_PATH,CHECKPOINT_FILE, EMBEDDINGS_FILE, BATCH

import click
from flask.cli import with_appcontext
@click.command()
@with_appcontext
def attack():
    """Generate embeddings of Mitre ATT&CK techniques."""
    # save logs
    os.makedirs(MITRE_ATTACK_LOG_PATH) if not os.path.exists(MITRE_ATTACK_LOG_PATH) else None
    sys.stdout = Logger(MITRE_ATTACK_LOG_PATH)

    print(f'{RED}Download/Update data or not? Please input yes or no:{RESET}')
    if input() == 'yes':
        # 1. update mitre att&ck data
        update()

        # 2. update embeddings
        os.remove(CHECKPOINT_FILE) if os.path.exists(CHECKPOINT_FILE) else None
        os.makedirs(EMBEDDINGS_FILE) if not os.path.exists(EMBEDDINGS_FILE) else None

        format_dict: dict[tuple, np.array] = {}
        count: int = 1
        while True:
            # 分批处理
            checkpoint = load_checkpoint()
            if checkpoint >= BATCH * count:
                filename: str = 'mitre_att&ck_' + str(count) + '.pkl'
                with open(EMBEDDINGS_FILE / filename, 'wb') as f:
                    print(f'{BLUE}Batch Processing: saving results in {filename}{RESET}')
                    pickle.dump(format_dict, f)

                format_dict: dict[tuple, np.array] = {}
                count += 1

            try:
                if format_data(format_dict, count):  # 注意终止条件，如果内部不限制可能会绕过分批处理的设计
                    break
            except Exception as e:
                print(f"An error occurred: {e}")

        # 3. save embeddings
        if BATCH >= checkpoint:  # 未作分批处理
            filename: str = 'mitre_att&ck.pkl'
        else:
            filename: str = 'mitre_att&ck_' + str(count) + '.pkl'

        with open(EMBEDDINGS_FILE / filename, 'wb') as f:
            print(f'{BLUE}Batch Processing: saving results in {filename}{RESET}')
            pickle.dump(format_dict, f)

    print(calc_distance("grav is a file-based Web platform. Prior to version 1.7.42, the denylist introduced "
                  "in commit 9d6a2d to prevent dangerous functions from being executed via injection of malicious "
                  "templates was insufficient and could be easily subverted in multiple ways -- "
                  "(1) using unsafe functions that are not banned, (2) using capitalised callable names, and "
                  "(3) using fully-qualified names for referencing callables. Consequently, a low privileged attacker "
                  "with login access to Grav Admin panel and page creation/update permissions "
                  "is able to inject malicious templates to obtain remote code execution. "
                  "A patch in version 1.7.42 improves the denylist."))
