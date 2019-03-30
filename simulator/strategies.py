from fireplace import game

from mcts.mcts import MCTS
from simulator import printer
from simulator.strategies_greedy import choose_card_from_hand, attack_opponent, \
    ChooseCard, AttackOpponent
from enum import IntEnum


class Strategies(IntEnum):
    RANDOM = 0
    AGGRESSIVE = 1
    CONTROLLING = 2
    MCTS = 3


def play_turn_using_strategy(game: ".game.Game", strategy, move_number):
    if strategy == Strategies.RANDOM:
        random_agent(game)
    elif strategy == Strategies.AGGRESSIVE:
        aggressive_agent(game)
    elif strategy == Strategies.CONTROLLING:
        controlling_agent(game)
    elif strategy == Strategies.MCTS:
        mcts_agent(game, move_number)


def random_agent(game: ".game.Game") -> ".game.Game":
    choose_card_from_hand(game, ChooseCard.RANDOM)
    attack_opponent(game, AttackOpponent.RANDOM)


def aggressive_agent(game: ".game.Game") -> ".game.Game":
    choose_card_from_hand(game, ChooseCard.OPTIMAL_COST)
    attack_opponent(game, AttackOpponent.AGGRESSIVE)


def controlling_agent(game: ".game.Game") -> ".game.Game":
    choose_card_from_hand(game, ChooseCard.OPTIMAL_COST)
    attack_opponent(game, AttackOpponent.CONTROLLING)


def mcts_agent(game: ".game.Game", move_number) -> ".game.Game":
    mcts = MCTS(game, move_number)
    cards_to_choose, cards_attack = mcts.choose_next_move()
    choose_card_from_hand(game, ChooseCard.DEFINED_CARDS, cards_to_choose)
    attack_opponent(game, AttackOpponent.DEFINED_CARDS, cards_attack)

    # for player in game.players:
    #     printer.print_player_cards(player)
