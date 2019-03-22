# Copyright (C) by Brett Kromkamp 2011-2014 (brett@perfectlearn.com)
# You Programming (http://www.youprogramming.com)
# May 03, 2014

# Modified by Łukasz Sus, Edyta Rogula
# 21st March 2019
import copy

from simulator.game import play_random_playout_from_state


class MCTSNode:
    def __init__(self, identifier, game):
        self.__identifier = identifier
        self.__num_wins = 0
        self.__num_playouts = 0
        self.__game = copy.deepcopy(game)
        self.__children = []
        self.__parent = None

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
        # TODO: przemyśleć, co z identifiers
        identifier.__parent = self
        self.__children.append(identifier)

    def random_playout(self):
        # TODO: sprawdzić
        game = copy.deepcopy(self.game)
        game, winner = play_random_playout_from_state(game)
        self.__num_playouts += 1
        if winner.name == "player1":    # zakladamy, ze player1 to "nasz" gracz MCTS
            self.__num_wins += 1

    def backpropagate(self):
        # TODO przekazać wynik playoutu do wyższych nodeów
        pass

    def expansion(self):
        # TODO stworzenie dzieci
        pass
