import random

from fireplace import game
from hearthstone.enums import CardType

from simulator.strategies_utils import choose_card_from_hand, attack_opponent, \
    choose_card_from_hand_sorting, ChooseCard, AttackOpponent
from simulator.printer import print_attack, print_player_cards
from enum import IntEnum


class Strategies(IntEnum):
    RANDOM = 0
    AGGRESIVE = 1
    CONTROLLING = 2
    MCTS = 3


def random_agent(game: ".game.Game") -> ".game.Game":
    player = game.current_player

    while True:
        # we don't want hero power, so it's commented below
        # heropower = player.hero.power
        # if heropower.is_usable() and random.random() < 0.1:
        #     if heropower.requires_target():
        #         heropower.use(target=random.choice(heropower.targets))
        #     else:
        #         heropower.use()
        #     continue

        # iterate over our hand and play whatever is playable
        for card in player.hand:
            if card.is_playable() and random.random() < 0.5:  # choose random cards
                target = None
                if card.must_choose_one:  # there are some choosable special skills
                    card = random.choice(card.choose_cards)
                if card.requires_target():  #
                    target = random.choice(card.targets)
                print("Playing %r on %r" % (card, target))
                card.play(target=target)

                if player.choice:  # chyba wybiera jakąś kartę???
                    choice = random.choice(player.choice.cards)
                    print("Choosing card %r" % (choice))
                    player.choice.choose(choice)

                continue

        # Randomly attack with whatever can attack
        for character in player.characters:
            if character.can_attack():
                target = random.choice(character.targets)
                character.attack(target)
                print_attack(character, target)

        break


def aggresive_agent(game: ".game.Game") -> ".game.Game":
    choose_card_from_hand(game, ChooseCard.OPTIMAL_COST)
    attack_opponent(game, AttackOpponent.AGGRESIVE)



def controlling_agent(game: ".game.Game") -> ".game.Game":
    pass
