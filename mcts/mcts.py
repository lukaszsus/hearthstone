import copy
import os
import random
import re
from itertools import chain, combinations, combinations_with_replacement, permutations

from fireplace import logging
from hearthstone.enums import Zone

from mcts.mctsnode import MCTSNode, NodeType
from mcts.mctstree import MCTSTree, IdGenerator
from research.saver import parse_to_dir_name, parse_to_file_name, save_lightweight_tree_to_file, create_if_not_exists, \
    SAVE_PATH
from simulator import printer


class MCTS:

    def __init__(self, game, move_number):
        self._game = copy.deepcopy(game)
        self._move_number = move_number
        self._tree = MCTSTree()
        self._root_id = self._tree.id_gen.get_next()
        self._tree.add_node(self._root_id, game=copy.deepcopy(self._game), type=NodeType.CHOOSE_CARD)     # root initialized
        self.player = self._game.current_player

    def choose_next_move(self):
        logger = logging.get_logger("fireplace")
        logger_before_state = logger.disabled
        logger.disabled = True

        self._tree.selection()

        cards_to_choose = []
        cards_attack = {}

        # self._tree.display(self._root_id)

        current_id = self._root_id
        while self._tree[current_id].player.name == self.player.name:
            if current_id is not None:
                if self._tree[current_id].chosen is not None:
                    if 'cards' in self._tree[current_id].chosen.keys():
                        cards_to_choose.extend(self._tree[current_id].chosen['cards'])
                    if 'attack' in self._tree[current_id].chosen.keys():
                        cards_attack[self._tree[current_id].chosen['attack'][0]] = self._tree[current_id].chosen['attack'][1]
            max_games = 0
            next_id = None
            for child in self._tree[current_id].children:
                if self._tree[child].num_playouts > max_games:
                    max_games = self._tree[child].num_playouts
                    next_id = child
            if next_id is not None:
                current_id = next_id
            else:
                break

        # self._save_tree()
        logger.disabled = logger_before_state
        return cards_to_choose, cards_attack

    def _save_tree(self):
        session_start = self._game.session_start
        dir_name = parse_to_dir_name(str(session_start))
        file_name = parse_to_file_name(self._game.id, self._move_number)
        path = os.path.join(SAVE_PATH, dir_name)
        create_if_not_exists(path)
        path = os.path.join(path, file_name)
        save_lightweight_tree_to_file(self._tree, path)


# def get_possible_choices_of_cards_from_hand(game: ".game.Game"):
#     player = game.current_player
#
#     possible_cards_choices = list()
#     for card_set in chain.from_iterable(combinations(player.hand, n) for n in range(len(player.hand) + 1)):
#         card_set = list(card_set)
#         sum_cost = sum(c.cost for c in card_set)
#         if sum_cost <= player.mana:
#             possible_cards_choices.append(card_set)
#     # TODO Nie wiem czy nie powinniśmy gdzieś sprawdzać warunku: if card.is_playable()
#     return possible_cards_choices


def generate_games_with_all_possible_choices_of_cards(game: "simulator.game.Game") -> list:
    """Zamiast generować wszystkie możliwe ruchy i potem je wykonywać,
    możemy od razu wygenerować gry z wszystkimi możliwymi stanami.
    I tak później musielibyśmy to zrobić, a tak jest prościej zaimplementować."""

    player = game.current_player
    possible_games = list()
    num_combinations_done = 0

    for card_set in chain.from_iterable(combinations(player.hand, n) for n in range(len(player.hand)+1)):
        num_combinations_done += 1
        card_set = list(card_set)
        sum_cost = sum(c.cost for c in card_set)
        if sum_cost <= player.mana:
            # ten wybór kart jest możliwy, więc tworzymy kopię gry i zagrywamy karty zgodnie z wyborem
            possible_games.append(copy.deepcopy(game))

            new_game_player = possible_games[-1].current_player
            new_card_set = recreate_card_choice(new_game_player, num_combinations_done)
            play_chosen_cards(new_game_player, new_card_set)

    return possible_games


def recreate_card_choice(new_game_player: "simulator.game.Player", num_combinations_done):
    """Funkcja combinations powinna być deterministyczna, więć odtwarzamy wybór kart w nowej grze."""
    i = 0
    for new_card_set in chain.from_iterable(
            combinations(new_game_player.hand, n) for n in range(len(new_game_player.hand) + 1)):
        i += 1
        if i == num_combinations_done:
            break
    return list(new_card_set)


def play_chosen_cards(new_game_player: "simulator.game.Player", new_card_set: list):
    for card in new_card_set:
        if card.is_playable():  # choose best cards from hand
            target = None
            if card.must_choose_one:  # there are some choosable special skills
                card = random.choice(card.choose_cards)
            if card.requires_target():  #
                target = random.choice(card.targets)
            print("Playing %r on %r" % (card, target))
            card.play(target=target)

            if new_game_player.choice:  # chyba wybiera jakąś kartę???
                choice = random.choice(new_game_player.choice.cards)
                print("Choosing card %r" % (choice))
                new_game_player.choice.choose(choice)


def generate_games_with_all_possible_choices_of_attacks(game: "simulator.game.Game") -> list:
    """Biblioteka itertools nie dostarcza wariacji z powtórzeniami,
    nawet nie znalazłem takiego pojęcia po angielsku. Aby najprościej stworzyć wariacje,
    wykonuję wszystkie kombinacje z powtórzeniami preciwników i wszystkie permutacje kart gracza.
    Nie jest to rozwiązanie dosłe, ponieważ powoduje powtórzenia,
    jeżeli nastąpi powtórzenie w kombinacji. Poza tym dobrze byłoby sprawdzać i wyrzucać przypadki,
    w których kolejny stworek atakuje już zabitego w tej kolejce przeciwnika, ale jest to nieco trudne.
    Posłguję się indeksami, aby móc to potem odtworzyć (spodziewkonaam się, że karty to też obiekty)."""

    player = game.current_player

    if len(player.characters) != 0:
        num_targets = len(player.characters[0].targets)
    else:
        num_targets = 0
    num_targets += 1        # na None - brak ataku
    num_characters = len(player.characters)

    characters_permutations = list(permutations(range(num_characters)))
    possible_targets = list(combinations_with_replacement(range(num_targets), num_characters))

    possible_games = list()
    for char_perm in characters_permutations:
        for poss_target in possible_targets:
            possible_games.append(copy.deepcopy(game))
            attack_chosen_if_possible(possible_games[-1], char_perm, poss_target)

    return possible_games


def attack_chosen_if_possible(game: "simulator.game.Game", character_indices: list, target_indices: list):
    player = game.current_player

    characters = [player.characters[index] for index in character_indices]

    for i in range(len(characters)):
        if characters[i].can_attack():
            if target_indices[i] >= len(characters[i].targets):
                continue
            else:
                target = characters[i].targets[target_indices[i]]
                if target.zone == Zone.PLAY:
                    characters[i].attack(target)
