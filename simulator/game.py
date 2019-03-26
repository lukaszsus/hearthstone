import os.path
import random

from fireplace.exceptions import GameOver

import simulator.printer as printer

from bisect import bisect
from importlib import import_module
from pkgutil import iter_modules
from typing import List
from xml.etree import ElementTree

from hearthstone.enums import CardClass, CardType
# Autogenerate the list of cardset modules
from simulator.game_utils import setup_game, play_turn
from simulator.strategies import Strategies


def play_full_game() -> ".game.Game":
    game = setup_game()

    for player in game.players:
        player.choice.choose()

    game.player1.strategy = Strategies.AGGRESSIVE
    game.player2.strategy = Strategies.CONTROLLING
    try:
        printer.print_main_phase_start()
        while True:
            player = game.current_player
            if player.name == 'Player1':
                play_turn(game, game.player1.strategy)

            if player.name == 'Player2':
                play_turn(game, game.player2.strategy)

            printer.print_empty_line()

    except GameOver:
        if game.player1.hero.health > game.player2.hero.health:
            print("{} WINS! {} : {}".format(game.player1.name, game.player1.hero.health, game.player2.hero.health))
        else:
            print("{} WINS! {} : {}".format(game.player2.name, game.player2.hero.health, game.player1.hero.health))

    return game
