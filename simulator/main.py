#!/usr/bin/env python
import sys

from fireplace import cards
from fireplace.exceptions import GameOver
from simulator.game import play_full_game

sys.path.append("..")


def test_full_game():
    try:
        play_full_game()
    except GameOver:
        print("Game completed normally.")


def main():
    cards.db.initialize() # inicjalizacja kart -> załadowanie wszystkich
    if len(sys.argv) > 1:
        numgames = sys.argv[1]
        if not numgames.isdigit():
            sys.stderr.write("Usage: %s [NUMGAMES]\n" % (sys.argv[0]))
            exit(1)
        for i in range(int(numgames)):
            test_full_game()
    else:
        test_full_game()


if __name__ == "__main__":
    main()
