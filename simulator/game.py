import os.path
import random

from fireplace.exceptions import GameOver

import simulator.printer as printer

from bisect import bisect
from importlib import import_module
from pkgutil import iter_modules
from typing import List
from xml.etree import ElementTree

from hearthstone.enums import CardClass, CardType, PlayState
# Autogenerate the list of cardset modules
from mcts.mctsnode import MCTSNode
from simulator.game_utils import setup_game, play_turn
from simulator.strategies import Strategies


def play_full_game(strategy_1=Strategies.RANDOM, strategy_2=Strategies.MCTS, game_id = -1, session_start = -1):
    game = setup_game()
    game.id = game_id
    game.session_start = session_start

    for player in game.players:
        player.choice.choose()

    if game.player1.name == 'Player1' and game.player2.name == 'Player2':
        game.player1.strategy = strategy_1
        game.player2.strategy = strategy_2
    elif game.player1.name == 'Player2' and game.player2.name == 'Player1':
        game.player1.strategy = strategy_2
        game.player2.strategy = strategy_1

    try:
        printer.print_main_phase_start()

        move_number = 0
        while True:
            player = game.current_player
            if player.name == 'Player1':
                play_turn(game, strategy_1, move_number)

            elif player.name == 'Player2':
                play_turn(game, strategy_2, move_number)
            move_number += 1
            printer.print_empty_line()

    except GameOver:
        winner = None
        if game.player1.playstate == PlayState.WON:
            print("{} ({}) WINS! {} : {}".format(game.player1.name, game.player1.strategy.name, game.player1.hero.health, game.player2.hero.health))
            winner = game.player1.name
        elif game.player2.playstate == PlayState.WON:
            print("{} ({}) WINS! {} : {}".format(game.player2.name, game.player2.strategy.name, game.player2.hero.health, game.player1.hero.health))
            winner = game.player2.name

    return game, winner
