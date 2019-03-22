import copy

from tree.node import MCTSNode


class MCTS:
    def __init__(self, game):
        self._game = copy.deepcopy(game)

    def choose_next_move(self):
        self._root = MCTSNode("root", game=self._game)
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