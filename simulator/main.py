#!/usr/bin/env python
import datetime
import sys

import numpy as np
from fireplace import cards, logging
from fireplace.exceptions import GameOver
from simulator.game import play_full_game
from simulator.strategies import Strategies

sys.path.append("..")


def test_full_game(strategy_1, strategy_2, id, session_start):
    try:
        play_full_game(strategy_1, strategy_2, id, session_start)
    except GameOver:
        print("Game completed normally.")


def main(strategy_1, strategy_2, id = -1, session_start = -1):
    cards.db.initialize() # inicjalizacja kart -> załadowanie wszystkich
    test_full_game(strategy_1, strategy_2, id, session_start)


if __name__ == "__main__":
    logger = logging.get_logger("fireplace")
    logger.disabled = True

    elapsed = []
    session_start = datetime.datetime.now()
    num_games = 20
    strategy_1 = Strategies.CONTROLLING
    strategy_2 = Strategies.MCTS

    for i in range(num_games):
        start = datetime.datetime.now()
        main(strategy_1, strategy_2, i, session_start)
        end = datetime.datetime.now()
        elapsed.append(end - start)
        print("\t{}. elapsed: {}".format(i, elapsed[i]))

    print(np.mean(elapsed))
