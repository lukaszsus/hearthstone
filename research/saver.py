import copy
import dill
import os
import pickle
import re


SAVE_PATH = '../trees/'
DIR_NAME = '2019-03-30-184125'


def create_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def parse_to_file_name(game_id, move_num) -> str:
    file_name = str(game_id).zfill(3)
    file_name += "_" + str(move_num).zfill(3) + ".pkl"
    return file_name


def parse_to_dir_name(dir_name: str) -> str:
    dir_name = str(dir_name)
    dir_name = dir_name.replace(":", "")
    dir_name = dir_name.replace(" ", "-")
    dir_name = re.search('.*\.', dir_name).group(0)
    dir_name = dir_name[:-1]
    return dir_name


def save_lightweight_tree_to_file(tree, file_path):
    # tree.display(tree._MCTSTree__root)
    light_tree = tree.get_lightweight_version()
    with open(file_path, 'wb') as output:
        # light_tree.display(light_tree._MCTSTree__root)
        dill.dump(light_tree, output, dill.HIGHEST_PROTOCOL)
