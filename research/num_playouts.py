import os
import re

import dill
import pandas as pd

import mcts
from research.leaves import get_game_move_id
from research.saver import SAVE_PATH, create_if_not_exists


def count_playouts(tree: mcts.mctstree):
    nodes = tree.get_all_nodes_identifiers()
    num_playouts = list()
    for node in nodes:
        num_playouts.append(tree[node].num_playouts)
    return sum(num_playouts), float(sum(num_playouts))/len(num_playouts)


def save_to_csv(dir_name, num_playouts, mean_num_playouts_per_node):
    columns = ["game", "move", "num_playouts", "mean_num_playouts_per_node"]
    data = pd.DataFrame(columns=columns)
    for game_id, dict in num_playouts.items():
        for move_id, num in dict.items():
            num_per_node = mean_num_playouts_per_node[game_id][move_id]
            row = pd.DataFrame(data=[[game_id, move_id, num, num_per_node]],
                               columns=columns)
            data = pd.concat([data, row], ignore_index=True)

    data = data.sort_values(['game', 'move'])
    data.game = data.game.astype(int)
    data.move = data.move.astype(int)
    dir_path = os.path.join(SAVE_PATH, dir_name)
    create_if_not_exists(dir_path)
    path = os.path.join(dir_path, 'playouts.csv')
    data.to_csv(path, index = False)


if __name__ == '__main__':
    for dir_name in os.listdir(SAVE_PATH):
        if re.search(".*_summary", dir_name):
            continue
        path = os.path.join(SAVE_PATH, dir_name)

        num_playouts = {}
        num_playouts_per_node = {}

        for file_name in os.listdir(path):
            game_id, move_id = get_game_move_id(file_name)
            file_path = os.path.join(path, file_name)
            with open(file_path, 'rb') as f:
                tree = dill.load(f)
                num, mean = count_playouts(tree)

                if game_id not in num_playouts_per_node:
                    num_playouts_per_node[game_id] = {move_id: mean}
                    num_playouts[game_id] = {move_id: num}
                else:
                    num_playouts_per_node[game_id][move_id] = mean
                    num_playouts[game_id][move_id] = num

                print("{} {}".format(str(game_id), str(move_id)))
        save_to_csv(dir_name + "_summary", num_playouts, num_playouts_per_node)