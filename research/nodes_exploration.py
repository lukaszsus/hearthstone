import os

import dill
import pandas as pd

import mcts
from research.leaves import get_game_move_id
from research.saver import SAVE_PATH, create_if_not_exists, DIR_NAME


def count_tree_expl_rate(tree: mcts.mctstree) -> float:
    nodes = tree.get_all_nodes_identifiers()
    rates = list()
    for node in nodes:
        if len(tree[node].children) != 0:
            rates.append(count_node_expl_rate(tree, node))
    return sum(rates)/len(rates)


def count_node_expl_rate(tree: mcts.mctstree, node: mcts.mctsnode) -> float:
    explored = 0
    not_explored = 0
    for child in tree[node].children:
        if tree[child].num_playouts != 0:
            explored += 1
        else:
            not_explored += 1
    return float(explored)/(explored+not_explored)


def save_to_csv(dir_name, means):
    columns = ["game", "move", "expl_rate"]
    data = pd.DataFrame(columns=columns)
    for game_id, moves_dict in means.items():
        for move_id, exlp_rate in moves_dict.items():
            row = pd.DataFrame(data=[[game_id, move_id, exlp_rate]],
                               columns=columns)
            data = pd.concat([data, row], ignore_index=True)

    data = data.sort_values(['game', 'move'])
    data.game = data.game.astype(int)
    data.move = data.move.astype(int)
    dir_path = os.path.join(SAVE_PATH, dir_name)
    create_if_not_exists(dir_path)
    path = os.path.join(dir_path, 'nodes_exploration.csv')
    data.to_csv(path, index = False)


if __name__ == '__main__':
    path = os.path.join(SAVE_PATH, DIR_NAME)

    expl_rates = {}

    for file_name in os.listdir(path):
        game_id, move_id = get_game_move_id(file_name)
        file_path = os.path.join(path, file_name)
        with open(file_path, 'rb') as f:
            tree = dill.load(f)

            if game_id not in expl_rates:
                expl_rates[game_id] = {move_id: count_tree_expl_rate(tree)}
            else:
                expl_rates[game_id][move_id] = count_tree_expl_rate(tree)

            print("{} {}".format(str(game_id), str(move_id)))
    save_to_csv(DIR_NAME + "_summary", expl_rates)