import datetime
import os
import re

import dill
import numpy as np
import pandas as pd

from research.leaves import get_game_move_id
from research.saver import SAVE_PATH, create_if_not_exists


def convert_str_to_date(str_time):
    str_time = str_time.replace("0 days ", "")
    str_time = re.search(".*\.", str_time).group(0)
    str_time = str_time.replace(".", "")
    time = datetime.datetime.strptime(str_time, '%H:%M:%S').time()
    seconds = time.second + time.minute*60 + time.hour*3600
    return seconds

def save_to_csv(dir_path, means):
    columns = ["game", "num_moves"]
    outcomes_path = os.path.join(dir_path, "outcomes.csv")
    outcomes = pd.read_csv(outcomes_path)

    if outcomes.shape[0] == len(means):
        outcomes['mean_num_moves'] = np.asarray(means)
    times = list()
    for mean in outcomes['mean_time_per_game']:
        times.append(convert_str_to_date(mean))
    times = np.asarray(times)
    outcomes['secods_per_game'] = times.transpose()
    times_per_move = np.asarray(outcomes['secods_per_game'])/np.asarray(outcomes['mean_num_moves'])
    outcomes['time_per_move'] = times_per_move

    path = os.path.join(dir_path, 'outcomes.csv')
    outcomes.to_csv(path, index = False)


if __name__ == '__main__':
    session_name  ="session_20190331_20190401"
    base_path = os.path.join('../outcomes/', session_name)
    means = list()
    last_dir_name = None
    dirs = os.listdir(base_path)
    dirs.sort()
    for dir_name in dirs:
        if re.search(".*_summary", dir_name):
            continue
        path = os.path.join(base_path, dir_name)

        num_moves = {}
        for file_name in os.listdir(path):
            game_id, move_id = get_game_move_id(file_name)
            if game_id not in num_moves:
                num_moves[game_id] = 1
            else:
                num_moves[game_id] += 1
            print("{} {}".format(str(game_id), str(move_id)))

        game_counter = 0
        move_couter = 0
        for game, value in num_moves.items():
            game_counter += 1
            move_couter += value
        means.append(float(move_couter)/game_counter)
        last_dir_name = dir_name

    path_to_save = os.path.join('../outcomes_summaries/', session_name)
    path_to_save = os.path.join(path_to_save, last_dir_name + "_summary")
    save_to_csv(path_to_save, means)