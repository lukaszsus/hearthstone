import random

from fireplace import game
from hearthstone.enums import CardType

from simulator.mcts import MCTS
from simulator.strategies_greedy import choose_card_from_hand, attack_opponent, \
    ChooseCard, AttackOpponent
from simulator.printer import print_attack, print_player_cards
from enum import IntEnum


class Strategies(IntEnum):
    RANDOM = 0
    AGGRESSIVE = 1
    CONTROLLING = 2
    MCTS = 3


def choose_agent(game: ".game.Game", strategy):
    if strategy == Strategies.RANDOM:
        random_agent(game)
    elif strategy == Strategies.AGGRESSIVE:
        aggressive_agent(game)
    elif strategy == Strategies.CONTROLLING:
        controlling_agent(game)
    elif strategy == Strategies.MCTS:
        mcts_agent(game)


def random_agent(game: ".game.Game") -> ".game.Game":
    choose_card_from_hand(game, ChooseCard.RANDOM)
    attack_opponent(game, AttackOpponent.RANDOM)


def aggressive_agent(game: ".game.Game") -> ".game.Game":
    choose_card_from_hand(game, ChooseCard.OPTIMAL_COST)
    attack_opponent(game, AttackOpponent.AGGRESSIVE)


def controlling_agent(game: ".game.Game") -> ".game.Game":
    choose_card_from_hand(game, ChooseCard.OPTIMAL_COST)
    attack_opponent(game, AttackOpponent.CONTROLLING)


def mcts_agent(game: ".game.Game") -> ".game.Game":
    mcts = MCTS(game)
    moves = mcts.choose_next_move()
    pass
