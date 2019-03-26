import copy
import random
from itertools import chain, combinations, combinations_with_replacement, permutations

from hearthstone.enums import Zone

from mcts.mctsnode import MCTSNode
from mcts.mctstree import MCTSTree


class MCTS:
    def __init__(self, game):
        self._game = copy.deepcopy(game)
        self._id_gen = IdGenerator()
        self._tree = MCTSTree()
        self._root_id = self._id_gen.get_next()
        self._tree.add_node(self._root_id, copy.deepcopy(self._game))     # root initialized

    def choose_next_move(self):
        self._root = MCTSNode("root", game=self._game)
        self._root.expansion()

        # zwraca kolejny ruch: jakie karty wybrać z ręki i co zaatakować
        # sugeruję to zrobić w taki sposób, że zwraca listę kart do wybrania z ręki
        # i listę dwuwymiarową z wszystkimi atakami naszych kart na karty przeciwnika (lub może słownik?)
        pass

    def make_one_step(self, game, moves):
        # jeden krok w grze zadany jako moves
        pass

    def best_child(self):
        # wybiera najlepsze dziecko z roota
        pass


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
    Nie jest to rozwiązanie doskonałe, ponieważ powoduje powtórzenia,
    jeżeli nastąpi powtórzenie w kombinacji. Poza tym dobrze byłoby sprawdzać i wyrzucać przypadki,
    w których kolejny stworek atakuje już zabitego w tej kolejce przeciwnika, ale jest to nieco trudne.
    Posłguję się indeksami, aby móc to potem odtworzyć (spodziewam się, że karty to też obiekty)."""

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


class IdGenerator:
    def __init__(self):
        self.__next_id = 0

    def get_next(self):
        to_ret = self.__next_id
        self.__next_id += 1
        return to_ret
