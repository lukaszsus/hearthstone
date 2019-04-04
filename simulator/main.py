#!/usr/bin/env python
import datetime
import os
import sys

import numpy as np
import pandas as pd
from fireplace import cards, logging
from fireplace.exceptions import GameOver

import mcts.mctstree as mctstree
from research.saver import SAVE_PATH, create_if_not_exists, parse_to_dir_name, parse_to_file_name
from simulator.game import play_full_game
from simulator.strategies import Strategies

sys.path.append("..")


def main(strategy_1, strategy_2, id = -1, session_start = -1):
    cards.db.initialize() # inicjalizacja kart -> załadowanie wszystkich
    _, winner = play_full_game(strategy_1, strategy_2, id, session_start)
    return winner


def save_to_file(session_start, data: pd.DataFrame):
    dir_name = parse_to_dir_name(str(session_start))
    dir_name += "_summary"
    dir_path = os.path.join(SAVE_PATH, dir_name)
    create_if_not_exists(dir_path)
    file_name = 'outcomes.csv'
    path = os.path.join(dir_path, file_name)
    data.to_csv(path, index=False)


def make_research():
    columns = ["Player1_strategy", "Player1_wins", "Player2_wins", "Player2_strategy", "mcts_time", "mean_time_per_game"]
    outcomes = pd.DataFrame(columns=columns)

    num_games = 100

    # strategies_to_test = [Strategies.AGGRESSIVE, Strategies.CONTROLLING, Strategies.RANDOM]
    strategies_to_test = [Strategies.RANDOM]
    strategy_2 = Strategies.MCTS

    # robię tutaj coś bardzo brzydkiego i traktuję bibliotekę jak obiekt, a jej stałą jak pole obiektu, ale działa
    for mctstree.MCTS_MAX_TIME in mctstree.MCTS_MAX_TIMES:
        for strategy_1 in strategies_to_test:
            session_start = datetime.datetime.now()
            elapsed = []
            player2_wins = 0
            for i in range(num_games):
                start = datetime.datetime.now()
                winner = main(strategy_1, strategy_2, i, session_start)
                if winner == 'Player2':
                    player2_wins += 1
                end = datetime.datetime.now()
                elapsed.append(end - start)
                print("\t{}. elapsed: {}".format(i, elapsed[i]))

            row = pd.DataFrame([[strategy_1.name, num_games - player2_wins, player2_wins, strategy_2.name,
                                 mctstree.MCTS_MAX_TIME, np.mean(elapsed)]], columns=columns)
            outcomes = pd.concat([outcomes, row], ignore_index=True)
            save_to_file(session_start, outcomes)
            print(np.mean(elapsed))


def make_short_game(num_games=10, strategy_1=Strategies.AGGRESSIVE, strategy_2=Strategies.MCTS):
    session_start = datetime.datetime.now()
    elapsed = []
    for i in range(num_games):
        start = datetime.datetime.now()
        main(strategy_1, strategy_2, i, session_start)
        end = datetime.datetime.now()
        elapsed.append(end - start)
        print("\t{}. elapsed: {}".format(i, elapsed[i]))


if __name__ == "__main__":
    logger = logging.get_logger("fireplace")
    logger.disabled = True
    # make_short_game()
    make_research()