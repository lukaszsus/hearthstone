import random
from enum import IntEnum
from itertools import chain, combinations

from hearthstone.enums import CardType

from simulator.printer import print_attack, print_playing_card_on_target, print_choosing_card


class ChooseCard(IntEnum):
    RANDOM = 0
    SORTED = 1
    OPTIMAL_COST = 2


class AttackOpponent(IntEnum):
    RANDOM = 0
    AGGRESSIVE = 1
    CONTROLLING = 2


def choose_card_from_hand(game: ".game.Game", strategy) -> ".game.Game":
    if strategy == ChooseCard.RANDOM:
        choose_card_from_hand_random(game)
    elif strategy == ChooseCard.SORTED:
        choose_card_from_hand_sorting(game)
    elif strategy == ChooseCard.OPTIMAL_COST:
        choose_card_from_hand_optimal_cost(game)


def attack_opponent(game: ".game.Game", strategy) -> ".game.Game":
    if strategy == AttackOpponent.RANDOM:
        attack_opponent_random(game)
    elif strategy == AttackOpponent.AGGRESSIVE:
        attack_opponent_aggresive(game)
    elif strategy == AttackOpponent.CONTROLLING:
        attack_opponent_controlling(game)


def choose_card_from_hand_sorting(game: ".game.Game") -> ".game.Game":
    player = game.current_player

    # prefer cards which are more expensive, have more atk and more health
    player.hand.sort(key=lambda x: (x.cost, x.atk, x.health), reverse=True)

    # iterate over our hand and play whatever is playable
    for card in player.hand:
        if card.is_playable():  # choose best cards from hand
            target = None
            if card.must_choose_one:  # there are some choosable special skills
                card = random.choice(card.choose_cards)
            if card.requires_target():  #
                target = random.choice(card.targets)
            print_playing_card_on_target(card, target)
            card.play(target=target)

            if player.choice:  # chyba wybiera jakąś kartę???
                choice = random.choice(player.choice.cards)
                print_choosing_card(choice)
                player.choice.choose(choice)


def choose_card_from_hand_optimal_cost(game: ".game.Game") -> ".game.Game":
    player = game.current_player

    max_cost = 0
    max_atk = 0
    max_health = 0
    chosen_cards = []
    for card_set in chain.from_iterable(combinations(player.hand, n) for n in range(len(player.hand)+1)):
        card_set = list(card_set)
        sum_cost = sum(c.cost for c in card_set)
        sum_atk = sum(c.atk for c in card_set)
        sum_health = sum(c.health for c in card_set)
        if max_cost < sum_cost <= player.mana:
            max_cost = sum_cost
            chosen_cards = card_set
        # jeżeli damy tutaj elif to funkcja zadziała niepoprawnie
        if max_cost == sum_cost and sum_atk > max_atk:
            max_atk = sum_atk
            chosen_cards = card_set

        if max_cost == sum_cost and sum_health > max_health:
            max_health = sum_health
            chosen_cards = card_set

    for card in chosen_cards:
        if card.is_playable():  # choose best cards from hand
            target = None
            if card.must_choose_one:  # there are some choosable special skills
                card = random.choice(card.choose_cards)
            if card.requires_target():  #
                target = random.choice(card.targets)
            print_playing_card_on_target(card, target)
            card.play(target=target)

            if player.choice:  # chyba wybiera jakąś kartę???
                choice = random.choice(player.choice.cards)
                print_choosing_card(choice)
                player.choice.choose(choice)


def choose_card_from_hand_random(game: ".game.Game") -> ".game.Game":
    player = game.current_player

    # iterate over our hand and play whatever is playable
    for card in player.hand:
        if card.is_playable() and random.random() < 0.5:  # choose random cards
            target = None
            if card.must_choose_one:  # there are some choosable special skills
                card = random.choice(card.choose_cards)
            if card.requires_target():  #
                target = random.choice(card.targets)
            print_playing_card_on_target(card, target)
            card.play(target=target)

            if player.choice:  # chyba wybiera jakąś kartę???
                choice = random.choice(player.choice.cards)
                print_choosing_card(choice)
                player.choice.choose(choice)


def attack_opponent_random(game: ".game.Game") -> ".game.Game":
    player = game.current_player

    for character in player.characters:
        if character.can_attack():
            target = random.choice(character.targets)
            character.attack(target)
            print_attack(character, target)


def attack_opponent_aggresive(game: ".game.Game") -> ".game.Game":
    player = game.current_player

    # Every cards attacks HERO if possible
    for character in player.characters:
        if character.can_attack():
            target = None
            for potential_target in character.targets:
                if potential_target.type == CardType.HERO:
                    target = potential_target
                    break
            if target is not None:
                character.attack(target)
                print_attack(character, target)


def attack_opponent_controlling(game: ".game.Game") -> ".game.Game":
    player = game.current_player

    # Every cards attacks another card if possible
    for character in player.characters:
        # prefer cards which have more atk and less health
        character.targets.sort(key=lambda x: (x.atk, -x.health), reverse=True)

        if character.can_attack():
            target = None
            for potential_target in character.targets:
                if potential_target.type == CardType.MINION:

                    if is_dead_after_attack(character, potential_target) and \
                            not is_dead_after_attack(potential_target, character):
                                # our character dies but the other doesn't
                                # so this attack doesn't make sense
                                pass
                    else:
                        target = potential_target
                        break

            if target is not None:
                character.attack(target)
                print_attack(character, target)

            else:  # if there are no minions on field or all are too strong
                for potential_target in character.targets:
                    if potential_target.type == CardType.HERO:
                        target = potential_target
                        break
                if target is not None:
                    character.attack(target)
                    print_attack(character, target)


def is_dead_after_attack(my_character, opponent_character):
    return my_character.health - opponent_character.atk <= 0
