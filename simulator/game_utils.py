import random
from bisect import bisect
from importlib import import_module
from pkgutil import iter_modules
from typing import List
from xml.etree import ElementTree

import os
from hearthstone.enums import CardType, CardClass

from simulator import printer
from simulator.strategies import choose_agent

_cards_module = os.path.join(os.path.dirname(__file__), "cards")
CARD_SETS = [cs for _, cs, ispkg in iter_modules([_cards_module]) if ispkg]

class CardList(list):
    def __contains__(self, x):
        for item in self:
            if x is item:
                return True
        return False

    def __getitem__(self, key):
        ret = super().__getitem__(key)
        if isinstance(key, slice):
            return self.__class__(ret)
        return ret

    def __int__(self):
        # Used in Kettle to easily serialize CardList to json
        return len(self)

    def contains(self, x):
        """
		True if list contains any instance of x
		"""
        for item in self:
            if x == item:
                return True
        return False

    def index(self, x):
        for i, item in enumerate(self):
            if x is item:
                return i
        raise ValueError

    def remove(self, x):
        for i, item in enumerate(self):
            if x is item:
                del self[i]
                return
        raise ValueError

    def exclude(self, *args, **kwargs):
        if args:
            return self.__class__(
                e for e in self for arg in args if e is not arg)
        else:
            return self.__class__(e for k, v in kwargs.items() for e in self if
                                  getattr(e, k) != v)

    def filter(self, **kwargs):
        return self.__class__(e for k, v in kwargs.items() for e in self if
                              getattr(e, k, 0) == v)


def random_draft(card_class: CardClass, exclude=[]):
    """
    Return a deck of 20 random cards for the \a card_class
    """
    from fireplace import cards
    from .deck import Deck

    deck = []
    collection = []
    # hero = card_class.default_hero

    minions = cards.filter(
            collectible=True,
            type=CardType.MINION,
            card_class=CardClass.NEUTRAL,
    )

    for card in minions:
        if card in exclude:
            continue
        cls = cards.db[card]
        if cls.cost > 10:
            continue
        collection.append(cls)

    while len(deck) < Deck.MAX_CARDS:
        card = random.choice(collection)
        if deck.count(card.id) < card.max_count_in_deck:
            deck.append(card.id)

    return deck


def shuffled_const_draft(card_indices):
    """
    Return a constant deck of 20 chosen cards for the \a card_class
    """
    from fireplace import cards
    from .deck import Deck

    deck = []
    collection = []

    minions = cards.filter(
            collectible=True,
            type=CardType.MINION,
            card_class=CardClass.NEUTRAL,
    )

    for card in minions:
        cls = cards.db[card]
        if cls.cost > 10 or len(cls.powers) > 0:  # filter cards that are too expensive or have any powers
            continue
        collection.append(cls)

    collection[:] = [collection[i] for i in card_indices]

    if len(collection) > Deck.MAX_CARDS/2:
        raise Exception("Too many cards chosen for deck.")

    for card in collection:
        deck.append(card.id)
        deck.append(card.id)    # every card doubled in deck

    random.shuffle(deck)
    return deck


def random_class():
    return CardClass(random.randint(2, 10))


def get_script_definition(id):
    """
    Find and return the script definition for card \a id
    """
    for cardset in CARD_SETS:
        module = import_module("fireplace.cards.%s" % (cardset))
        if hasattr(module, id):
            return getattr(module, id)


def entity_to_xml(entity):
    e = ElementTree.Element("Entity")
    for tag, value in entity.tags.items():
        if value and not isinstance(value, str):
            te = ElementTree.Element("Tag")
            te.attrib["enumID"] = str(int(tag))
            te.attrib["value"] = str(int(value))
            e.append(te)
    return e


def game_state_to_xml(game):
    tree = ElementTree.Element("HSGameState")
    tree.append(entity_to_xml(game))
    for player in game.players:
        tree.append(entity_to_xml(player))
    for entity in game:
        if entity.type in (CardType.GAME, CardType.PLAYER):
            # Serialized those above
            continue
        e = entity_to_xml(entity)
        e.attrib["CardID"] = entity.id
        tree.append(e)

    return ElementTree.tostring(tree)


def weighted_card_choice(source, weights: List[int], card_sets: List[str],
                         count: int):
    """
    Take a list of weights and a list of card pools and produce
    a random weighted sample without replacement.
    len(weights) == len(card_sets) (one weight per card set)
    """

    chosen_cards = []

    # sum all the weights
    cum_weights = []
    totalweight = 0
    for i, w in enumerate(weights):
        totalweight += w * len(card_sets[i])
        cum_weights.append(totalweight)

    # for each card
    for i in range(count):
        # choose a set according to weighting
        chosen_set = bisect(cum_weights, random.random() * totalweight)

        # choose a random card from that set
        chosen_card_index = random.randint(0, len(card_sets[chosen_set]) - 1)

        chosen_cards.append(card_sets[chosen_set].pop(chosen_card_index))
        totalweight -= weights[chosen_set]
        cum_weights[chosen_set:] = [x - weights[chosen_set] for x in
                                    cum_weights[chosen_set:]]

    return [source.controller.card(card, source=source) for card in
            chosen_cards]


def setup_game() -> ".game.Game":
    from fireplace.game import Game
    from simulator.player import Player

    # card_indices = [27, 48, 68, 159, 169, 180, 307, 386, 546, 588]  # randomly chosen 10 integers from [1,698]
    card_indices = [random.randrange(1, 28) for i in range(10)]

    deck1 = shuffled_const_draft(card_indices)  # choose cards for Player1
    deck2 = shuffled_const_draft(card_indices)  # choose cards for Player2

    printer.print_deck_content("Player1", deck1)
    printer.print_deck_content("Player2", deck2)

    player1 = Player("Player1", deck1, CardClass.MAGE.default_hero)
    player2 = Player("Player2", deck2, CardClass.MAGE.default_hero)

    game = Game(players=(player1, player2))
    game.start()

    player1.hero.set_current_health(20)
    player2.hero.set_current_health(20)

    return game


def play_turn(game: ".game.Game", strategy: int) -> ".game.Game":
    for player in game.players:
        printer.print_player_cards(player)

    player = game.current_player

    for character in player.hand:
        if character.type == CardType.SPELL:
            player.hand.remove(character)

    choose_agent(game, strategy)

    game.end_turn()
    return game

