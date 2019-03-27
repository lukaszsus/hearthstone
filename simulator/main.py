#!/usr/bin/env python
import datetime
import sys

import numpy as np
from fireplace import cards, logging
from fireplace.exceptions import GameOver
from simulator.game import play_full_game
from simulator.strategies import Strategies

sys.path.append("..")


def test_full_game(strategy_1, strategy_2):
    try:
        play_full_game(strategy_1, strategy_2)
    except GameOver:
        print("Game completed normally.")


def main(strategy_1, strategy_2):
    cards.db.initialize() # inicjalizacja kart -> załadowanie wszystkich
    test_full_game(strategy_1, strategy_2)


if __name__ == "__main__":
    logger = logging.get_logger("fireplace")
    logger.disabled = True

    elapsed = []
    strategy_1 = Strategies.RANDOM
    strategy_2 = Strategies.MCTS
    for _ in range(10):
        start = datetime.datetime.now()
        main(strategy_1, strategy_2)
        end = datetime.datetime.now()
        elapsed.append(end - start)

    print(np.mean(elapsed))
