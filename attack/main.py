import os.path
import pickle

from config import Config
from package import format_data
from prepare import update


if __name__ == '__main__':
    print(f'{Config.RED}Download/Update data or not? Please input yes or no:{Config.RESET}')
    if input() == 'yes':
        # 1. update mitre att&ck data
        update()

        # 2. update embeddings
        os.remove(Config.CHECKPOINT_FILE) if os.path.exists(Config.CHECKPOINT_FILE) else None

        format_list: list = []
        while True:
            try:
                if not format_data(format_list):
                    break
            except Exception as e:
                print(f"An error occurred: {e}")

        # 3. save embeddings
        with open(Config.EMBEDDINGS_FILE, 'wb') as f:
            pickle.dump(format_list, f)

    # 4. read embeddings
    # with open(Config.EMBEDDINGS_FILE, 'rb') as f:
    #     print(pickle.load(f))
