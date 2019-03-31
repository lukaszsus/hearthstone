import os
import re
import dill
import numpy as np
import pandas as pd

from mcts import mctstree
from research.saver import SAVE_PATH, create_if_not_exists


def get_game_move_id(file_name):
    base, ext = os.path.splitext(file_name)
    game_id = re.search(".*_", base).group(0)
    game_id = game_id.replace("_","")
    # game_id = int(game_id)
    move_id = re.search("_.*", base).group(0)
    move_id = move_id.replace("_", "")
    # move_id = int(move_id)
    return game_id, move_id


def count_depths(tree: mctstree) -> list:
    depths = list()
    nodes = tree.get_all_nodes_identifiers()
    for node in nodes:
        depths.append(count_node_depth(tree, node))
    return depths


def count_node_depth(tree, node) -> int:
    depth = 0
    while tree[node].parent is not None:
        depth += 1
        node = tree[node].parent
    return depth


def save_to_csv(dir_name, means, medians, maxes):
    columns = ["game", "move", "mean", "median", "max"]
    data = pd.DataFrame(columns=columns)
    for game_id, medians_dict in means.items():
        for move_id, mean in medians_dict.items():
            median = medians[game_id][move_id]
            max_ = maxes[game_id][move_id]
            row = pd.DataFrame(data=[[game_id, move_id, mean, median, max_]],
                               columns=columns)
            data = pd.concat([data, row], ignore_index=True)

    data = data.sort_values(['game', 'move'])
    data.game = data.game.astype(int)
    data.move = data.move.astype(int)
    dir_path = os.path.join(SAVE_PATH, dir_name)
    create_if_not_exists(dir_path)
    path = os.path.join(dir_path, 'leaves.csv')
    data.to_csv(path, index = False)


if __name__ == '__main__':
    for dir_name in os.listdir(SAVE_PATH):
        if re.search(".*_summary", dir_name):
            continue
        path = os.path.join(SAVE_PATH, dir_name)

        means = {}
        medians = {}
        maxes = {}

        for file_name in os.listdir(path):
            game_id, move_id = get_game_move_id(file_name)
            file_path = os.path.join(path, file_name)
            with open(file_path, 'rb') as f:
                tree = dill.load(f)
                depths = np.asarray(count_depths(tree))
                mean = depths.mean()
                median = np.median(depths)
                max_ = depths.max()

                if game_id not in means:
                    means[game_id] = {move_id: mean}
                else:
                    means[game_id][move_id] = mean
                if game_id not in medians:
                    medians[game_id] = {move_id: median}
                else:
                    medians[game_id][move_id] = median
                if game_id not in maxes:
                    maxes[game_id] = {move_id: max_}
                else:
                    maxes[game_id][move_id] = max_
                print("{} {}".format(str(game_id), str(move_id)))
        save_to_csv(dir_name + "_summary", means, medians, maxes)