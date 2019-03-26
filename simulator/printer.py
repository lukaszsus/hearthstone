from fireplace.player import Player
from simulator.deck import Deck
from fireplace.logging import log


def print_player_cards(player: Player):
    cards = player.name + " hero: " + str(player.hero) \
            + "(" + str(player.hero.health) + "); "
    cards = cards + " cards in field: "
    for character in player.field:
        try:
            cards = cards + str(character) + "({},{},{}); ".format(character.atk,
                                                             character.health,
                                                             character.cost)
        except:  # for Spell cards which don't have atk attribute
            cards = cards + str(character)
    cards = cards + " cards in hand: "
    for character in player.hand:
        try:
            cards = cards + str(character) + "({},{},{}); ".format(character.atk,
                                                             character.health,
                                                             character.cost)
        except:  # for Spell cards which don't have atk attribute
            cards = cards + str(character)
    log.info("#" + cards)


def print_deck_content(player_name: str, deck: Deck):
    deck_info = player_name + "'s deck contains:\n {0}".format(deck)
    log.info("#" + deck_info)


def print_attack(character, target):
    log.info("# {}({},{},{}) attacks {}({},{},{})".format(str(character),
                                                          character.atk,
                                                          character.health,
                                                          character.cost,
                                                          str(target),
                                                          target.atk,
                                                          target.health,
                                                          target.cost,
                                                          ))


def print_main_phase_start():
    log.info("\n")
    log.info("Main phase of game starts.")


def print_empty_line():
    log.info("\n")


def print_playing_card_on_target(card, target):
    log.info("Playing %r on %r" % (card, target))


def print_choosing_card(choice):
    log.info("Choosing card %r" % (choice))
