import os.path
import pickle
import sys

from log.log import Logger
from config import Config
from package import format_data, load_checkpoint
from prepare import update


if __name__ == '__main__':
    # save logs
    sys.stdout = Logger("./log/")

    print(f'{Config.RED}Download/Update data or not? Please input yes or no:{Config.RESET}')
    if input() == 'yes':
        # 1. update mitre att&ck data
        update()

        # 2. update embeddings
        os.remove(Config.CHECKPOINT_FILE) if os.path.exists(Config.CHECKPOINT_FILE) else None
        os.makedirs(Config.EMBEDDINGS_FILE) if not os.path.exists(Config.EMBEDDINGS_FILE) else None

        format_list: list = []
        count: int = 1
        while True:
            # 分批处理
            checkpoint = load_checkpoint()
            if checkpoint >= Config.BATCH * count:
                filename: str = 'mitre_att&ck_' + str(count) + '.pkl'
                with open(Config.EMBEDDINGS_FILE + filename, 'wb') as f:
                    print(f'{Config.BLUE}Batch Processing: saving results in {filename}{Config.RESET}')
                    pickle.dump(format_list, f)

                format_list: list = []
                count += 1

            try:
                if format_data(format_list, count):  # 注意终止条件，如果内部不限制可能会绕过分批处理的设计
                    break
            except Exception as e:
                print(f"An error occurred: {e}")

        # 3. save embeddings
        filename: str = 'mitre_att&ck_' + str(count) + '.pkl'
        with open(Config.EMBEDDINGS_FILE + filename, 'wb') as f:
            print(f'{Config.BLUE}Batch Processing: saving results in {filename}{Config.RESET}')
            pickle.dump(format_list, f)

    # 4. read embeddings
    # with open(Config.EMBEDDINGS_FILE, 'rb') as f:
    #     print(pickle.load(f))
