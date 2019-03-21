import copy

from tree.node import Node


class MCTS:
    def __init__(self):
        # tu na pewno potrzebujemy stworzyć początkowe drzewo
        # ważne: musimy mieć jeden obiekt tej klasy dla jednego gracza - nie może powstawać nowy obiekt w funkcji mcts_agent
        pass

    def choose_next_move(self, game: ".game.Game"):
        self._game = copy.deepcopy(game)
        self._root = Node("root", game=self._game)
        # zwraca kolejny ruch: jakie karty wybrać z ręki i co zaatakować
        # sugeruję to zrobić w taki sposób, że zwraca listę kart do wybrania z ręki
        # i listę dwuwymiarową z wszystkimi atakami naszych kart na karty przeciwnika (lub może słownik?)
        pass

    def selection(self):
        # zaczynając od korzenia drzewa R, wybieraj kolejne węzły potomne, aż dotrzesz do liścia drzewa L.
        pass

    def expansion(self):
        # o ile L nie kończy gry, utwórz w nim jeden lub więcej węzłów potomnych i wybierz z nich jeden węzeł C.
        pass

    def playout(self):
        # rozegraj losową symulację z węzła C
        pass

    def backpropagation(self):
        # na podstawie wyniku rozegranej symulacji uaktualnij informacje w węzłach na ścieżce prowadzącej od C do R.
        pass
