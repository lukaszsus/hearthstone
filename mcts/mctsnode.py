# Copyright (C) by Brett Kromkamp 2011-2014 (brett@perfectlearn.com)
# You Programming (http://www.youprogramming.com)
# May 03, 2014

# Modified by Łukasz Sus, Edyta Rogula
# 21st March 2019
import copy
from enum import IntEnum
from itertools import chain, combinations

from logging import basicConfig, WARNING, DEBUG

from fireplace import logging
from fireplace.exceptions import GameOver
from hearthstone.enums import CardType, PlayState

from simulator import printer
from simulator.strategies_greedy import choose_card_from_hand_defined, attack_opponent_defined


class NodeType(IntEnum):
    NONE = 0
    CHOOSE_CARD = 1
    ATTACK = 2
    END_TURN = 3


class MCTSNode:
    def __init__(self, identifier, game, type=NodeType.NONE, chosen=None):
        self.__identifier = identifier
        self.__num_wins = 0
        self.__num_playouts = 0
        self.__game = copy.deepcopy(game)
        self.__children = []
        self.__parent = None
        self.player = game.current_player
        self.next_node_type = type
        self.chosen = chosen

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

    def random_playout(self, tree):
        game = copy.deepcopy(self.game)
        _, winner = self._play_random_playout_from_state()
        self.game = game
        self.backpropagate(winner, tree)

    def backpropagate(self, winner, tree):
        self.__num_playouts += 1
        if winner == self.player.name:
            self.__num_wins += 1
        if self.parent is not None:
            tree[self.parent].backpropagate(winner, tree)

    def expansion(self, tree):
        if self.next_node_type == NodeType.CHOOSE_CARD:
            # ruch związany z wyborem kart - kolejny będzie z atakiem
            self.add_nodes_with_all_possible_card_choices(tree)
        elif self.next_node_type == NodeType.ATTACK:
            # ruch związany z atakowaniem - kolejny będzie ruch niedeterministyczny z ciągnięciem kart itp.
            # chyba najsensowniej będzie robić jeden ruch (node) osobny dla każdej karty, która może atakować?
            self.add_nodes_with_all_possible_attacks(tree)
        elif self.next_node_type == NodeType.END_TURN:
            # ruch niedeterministyczny (?) - ciągnięcie karty, zmiana playerów etc.
            game = copy.deepcopy(self.game)
            game.end_turn()
            tree.add_node(identifier=tree.id_gen.get_next(), game=game,
                          type=NodeType.CHOOSE_CARD, parent=self.identifier, chosen=None)

    def add_nodes_with_all_possible_card_choices(self, tree):
        # wszystkie nowe nody - type NodeType.ATTACK
        for card_set in chain.from_iterable(combinations(self.player.hand, n) for n in range(len(self.player.hand) + 1)):
            sum_cost = sum(c.cost for c in card_set)
            card_set = [c.uuid for c in card_set]
            if sum_cost <= self.player.mana:
                game = copy.deepcopy(self.game)
                game = choose_card_from_hand_defined(game, card_set)
                tree.add_node(identifier=tree.id_gen.get_next(), game=game,
                              type=NodeType.ATTACK, parent=self.identifier, chosen={'cards': card_set})

    def add_nodes_with_all_possible_attacks(self, tree):
        # nowe nody - type NodeType.END_TURN
        num_attacks = 0
        # TODO: sprawdzić, czy dodają się więcej niż jedne nody z atakami
        for character in self.player.characters:
            if character.type == CardType.MINION and character.can_attack():
                num_attacks += 1
                for target in character.targets:
                    game = copy.deepcopy(self.game)
                    game = attack_opponent_defined(game, {character.uuid : target.uuid})
                    tree.add_node(identifier=tree.id_gen.get_next(), game=game,
                                  type=NodeType.ATTACK, parent=self.identifier,
                                  chosen={'attack': [character.uuid, target.uuid]})
                break
        if num_attacks == 0:
            game = copy.deepcopy(self.game)
            tree.add_node(identifier=tree.id_gen.get_next(), game=game,
                          type=NodeType.END_TURN, parent=self.identifier, chosen=None)

    def _play_random_playout_from_state(self) -> (".game.Game", ".player.Player"):
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
            if game.player1.playstate == PlayState.WON:
                winner = game.player1.name
                # print("{} WINS! {} : {}".format(game.player1.name, game.player1.hero.health, game.player2.hero.health))
            elif game.player2.playstate == PlayState.WON:
                winner = game.player2.name
                # print("{} WINS! {} : {}".format(game.player2.name, game.player2.hero.health, game.player1.hero.health))

        return game, winner

    @game.setter
    def game(self, value):
        self.__game = value

    @parent.setter
    def parent(self, value):
        self.__parent = value
