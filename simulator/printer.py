from fireplace.player import Player
from simulator.deck import Deck
from fireplace.logging import log


def print_player_cards(player: Player):
    cards = player.name + " cards in field: "
    for character in player.field:
        try:
            cards = cards + character.id + "({},{},{}); ".format(character.atk,
                                                             character.max_health,
                                                             character.cost)
        except:  # for Spell cards which don't have atk attribute
            cards = cards + character.id
    cards = cards + " cards in hand: "
    for character in player.hand:
        try:
            cards = cards + character.id + "({},{},{}); ".format(character.atk,
                                                             character.max_health,
                                                             character.cost)
        except:  # for Spell cards which don't have atk attribute
            cards = cards + character.id
    log.info("#" + cards)


def print_deck_content(player_name: str, deck: Deck):
    deck_info = player_name + "'s deck contains:\n {0}".format(deck)
    log.info("#" + deck_info)
