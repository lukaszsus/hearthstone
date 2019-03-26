# Copyright (C) by Brett Kromkamp 2011-2014 (brett@perfectlearn.com)
# You Programming (http://www.youprogramming.com)
# May 03, 2014

# Modified by Łukasz Sus, Edyta Rogula
# 21st March 2019
import copy
from enum import IntEnum

from logging import basicConfig, WARNING, DEBUG

from fireplace import logging
from fireplace.exceptions import GameOver
from simulator import printer


class NodeType(IntEnum):
    NONE = 0
    CHOOSE_CARD = 1
    ATTACK = 2
    END_TURN = 3


class MCTSNode:
    def __init__(self, identifier, game, type=NodeType.NONE):
        self.__identifier = identifier
        self.__num_wins = 0
        self.__num_playouts = 0
        self.__game = copy.deepcopy(game)
        self.__children = []
        self.__parent = None
        self.player = game.current_player
        self.type = type

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
        self.__children.append(identifier)

    def random_playout(self):
        # TODO: sprawdzić
        game = copy.deepcopy(self.game)
        _, winner = self._play_random_playout_from_state()
        self.game = game
        self.backpropagate(winner)

    def backpropagate(self, winner):
        # TODO sprawdzić
        self.__num_playouts += 1
        if winner.name == self.player:
            self.__num_wins += 1
        if self.parent is not None:
            self.parent.backpropagate(winner)

    def expansion(self, tree):
        # TODO stworzenie dzieci tego node'a
        # get all possible moves
        # append them as children
        if self.type == NodeType.CHOOSE_CARD:
            # ruch związany z wyborem kart - kolejny będzie z atakiem
            self.add_nodes_with_all_possible_card_choices()
        elif self.type == NodeType.ATTACK:
            # ruch związany z atakowaniem - kolejny będzie ruch niedeterministyczny z ciągnięciem kart itp.
            self.add_nodes_with_all_possible_attacks()
        elif self.type == NodeType.END_TURN:
            # ruch niedeterministyczny (?) - ciągnięcie karty, zmiana playerów etc.
            game = copy.deepcopy(self.game)
            game.end_turn()
            tree.add_node(identifier=tree.id_gen.get_next(), game=game,
                          type=NodeType.CHOOSE_CARD, parent=self.identifier)

    def add_nodes_with_all_possible_card_choices(self):
        # wszystkie nody - type NodeType.ATTACK
        pass

    def add_nodes_with_all_possible_attacks(self):
        # wszystkie nody - type NodeType.END_TURN
        pass

    def _play_random_playout_from_state(self) -> (".game.Game", ".player.Player"):
        logger = logging.get_logger("fireplace")
        logger.disabled = True
        # stop printing logger messages for random playouts

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
                # print("{} WINS! {} : {}".format(game.player1.name, game.player1.hero.health, game.player2.hero.health))
            else:
                winner = game.player2.name
                # print("{} WINS! {} : {}".format(game.player2.name, game.player2.hero.health, game.player1.hero.health))

        logger.disabled = False  # start printing logger messages
        return game, winner

    @game.setter
    def game(self, value):
        self._game = value

    @parent.setter
    def parent(self, value):
        self._parent = value
