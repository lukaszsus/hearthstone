# Brett Kromkamp (brett@perfectlearn.com)
# You Programming (http://www.youprogramming.com)
# May 03, 2014
import random

import numpy as np

from mcts.mctsnode import MCTSNode, NodeType

(_ROOT, _DEPTH, _BREADTH) = range(3)


class MCTSTree:

    def __init__(self):
        self.__nodes = {}
        self.id_gen = IdGenerator()
        self.__root = None
        self.exploration_param = np.sqrt(2)  # być może trzeba to dostosować, ale na razie niech będzie

    @property
    def nodes(self):
        return self.__nodes

    def add_node(self, identifier, game, type=NodeType.NONE, parent=None, chosen=None):
        node = MCTSNode(identifier, game=game, type=type, chosen=chosen)

        if len(self.__nodes) == 0:
            self.__root = identifier

        self[identifier] = node

        if parent is not None:
            self[identifier].parent = parent
            self[parent].add_child(identifier)

        return node

    def display(self, identifier, depth=_ROOT):
        children = self[identifier].children
        if depth == _ROOT:
            print("{0}({1}/{2})".format(identifier, self[identifier].num_wins, self[identifier].num_playouts))
        else:
            print("\t"*depth, "{0}({1}/{2})".format(identifier, self[identifier].num_wins, self[identifier].num_playouts))

        depth += 1
        for child in children:
            self.display(child, depth)  # recursive call

    def traverse(self, identifier, mode=_DEPTH):
        # Python generator. Loosly based on an algorithm from
        # 'Essential LISP' by John R. Anderson, Albert T. Corbett,
        # and Brian J. Reiser, page 239-241
        yield identifier
        queue = self[identifier].children
        while queue:
            yield queue[0]
            expansion = self[queue[0]].children
            if mode == _DEPTH:
                queue = expansion + queue[1:]  # depth-first
            elif mode == _BREADTH:
                queue = queue[1:] + expansion  # width-first

    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item

    def selection(self):
        # TODO sprawdzić
        current_id = self.__root
        i = 0
        while i < 100:  # TODO: warunek inny???
            i += 1
            try:
                unvisited_child = random.choice(self.get_unvisited(self[current_id].children))
                self[unvisited_child].random_playout(self)
                current_id = self.__root
                continue
            except IndexError:
                # when selected_child is None, because get_unvisited is empty
                # which means all children nodes were visited - we have to select one of them!
                max_ucts = 0
                selected_child = None
                if len(self[current_id].children) == 0:
                    self[current_id].expansion(self)
                    continue
                for child in self[current_id].children:
                    # TODO: check this ucts value, probably use something else for selection???
                    ucts = self[child].num_wins / self[child].num_playouts + self.exploration_param * \
                           np.sqrt(np.log(self[self.__root].num_playouts) / self[child].num_playouts)
                    if ucts >= max_ucts:
                        max_ucts = ucts
                        selected_child = child
                current_id = selected_child
                continue

    def get_unvisited(self, children):
        unvisited = []
        for child in children:
            if self[child].num_playouts == 0:
                unvisited.append(child)
        return unvisited


class IdGenerator:
    def __init__(self):
        self.__next_id = 0

    def get_next(self):
        to_ret = self.__next_id
        self.__next_id += 1
        return to_ret
