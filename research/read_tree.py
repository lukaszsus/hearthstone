import os

import dill

from research.saver import SAVE_PATH

if __name__ == '__main__':
    dir_name = '2019-03-30-184125'
    dir_path = os.path.join(SAVE_PATH, dir_name)

    file_name = '018_004.pkl'
    path = os.path.join(dir_path, file_name)
    with open(path, 'rb') as f:
        tree = dill.load(f)
        tree.display()

    # for file_name in os.listdir(dir_path):
    #     path = os.path.join(dir_path, file_name)
    #     with open(path, 'rb') as f:
    #         tree = dill.load(f)
    #         tree.display()