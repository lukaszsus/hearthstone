# Copyright (C) by Brett Kromkamp 2011-2014 (brett@perfectlearn.com)
# You Programming (http://www.youprogramming.com)
# May 03, 2014

# Modified by Łukasz Sus, Edyta Rogula
# 21st March 2019
import copy

from fireplace.exceptions import GameOver
from simulator import printer


class MCTSNode:
    def __init__(self, identifier, game):
        self.__identifier = identifier
        self.__num_wins = 0
        self.__num_playouts = 0
        self.__game = copy.deepcopy(game)
        self.__children = []
        self.__parent = None
        self.player = game.current_player

    @property
    def identifier(self):
        return self.__identifier

    @property
    def children(self):
        return self.__children

    @property
    def num_wins(self):
        return self.__num_wins

    @property
    def num_playouts(self):
        return self.__num_playouts

    @property
    def game(self):
        return self.__game

    @property
    def parent(self):
        return self.__parent

    def add_child(self, identifier):
        # TODO: przemyśleć, co z identifiers!!!
        identifier.__parent = self
        self.__children.append(identifier)

    def random_playout(self):
        # TODO: sprawdzić
        game = copy.deepcopy(self.game)
        _, winner = self.play_random_playout_from_state()
        self.game = game
        self.backpropagate(winner)

    def backpropagate(self, winner):
        # TODO sprawdzić
        self.__num_playouts += 1
        if winner.name == self.player:
            self.__num_wins += 1
        if self.parent is not None:
            self.parent.backpropagate(winner)

    def expansion(self):
        # TODO stworzenie dzieci
        # get all possible moves
        # append them as children
        pass

    def play_random_playout_from_state(self) -> (".game.Game", ".player.Player"):
        from simulator.game_utils import play_turn
        from simulator.strategies import Strategies
        game = self.__game
        winner = None
        player1_strategy = Strategies.RANDOM
        player2_strategy = Strategies.RANDOM

        try:
            while True:
                player = game.current_player
                if player.name == 'Player1':
                    play_turn(game, player1_strategy)

                if player.name == 'Player2':
                    play_turn(game, player2_strategy)

                printer.print_empty_line()

        except GameOver:
            if game.player1.hero.health > game.player2.hero.health:
                winner = game.player1.name
                print("{} WINS! {} : {}".format(game.player1.name, game.player1.hero.health, game.player2.hero.health))
            else:
                winner = game.player2.name
                print("{} WINS! {} : {}".format(game.player2.name, game.player2.hero.health, game.player1.hero.health))

        return game, winner

    @game.setter
    def game(self, value):
        self._game = value
