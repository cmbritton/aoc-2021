import math
import re
from typing import Tuple
import time
import ast
import itertools



class Tree(object):

    def __init__(self, root=None):
        self.root = root

    @staticmethod
    def from_list(sfn):
        tree = Tree(Tree._from_list(sfn))
        return tree

    @staticmethod
    def _from_list(sfn):
        node = Node(sfn, sfn[0], sfn[1])
        if type(sfn[0]) == list:
            node.left = Tree._from_list(sfn[0])
        elif type(sfn[0]) == int:
            node.left = Node(sfn[0])
        else:
            node.left = None

        if type(sfn[1]) == list:
            node.right = Tree._from_list(sfn[1])
        elif type(sfn[1]) == int:
            node.right = Node(sfn[1])
        else:
            node.right = None
        return node

    def find_node(self, node, value):
        if not node:
            return None
        if node.value == value:
            return node
        sub_node = self.find_node(node.left, value)
        if not sub_node:
            sub_node = self.find_node(node.right, value)
        return sub_node

    def path_to_root(self, node):
        path = []
        if node:
            path.append(node)
            sub_path = self.path_to_root(self.find_parent(self.root, node))
            if sub_path:
                path.extend(sub_path)
        return path

    def distance_to_root(self, node):
        return len(self.path_to_root(node))

    def find_parent(self, current_node, target_node):
        if not current_node:
            return None
        if current_node.left == target_node or current_node.right == target_node:
            return current_node
        node = self.find_parent(current_node.left, target_node)
        if not node:
            node = self.find_parent(current_node.right, target_node)
        return node

    def nodes(self):
        return self._nodes(self.root)

    def _nodes(self, node):
        result = []
        if node.left:
            result.extend(self._nodes(node.left))
        result.append(node)
        if node.right:
            result.extend(self._nodes(node.right))

        return result

    def leaf_nodes(self):
        return self._leaf_nodes(self.root)

    def _leaf_nodes(self, node):
        if node.is_leaf():
            return [node]

        result = []
        if node.left:
            result.extend(self._leaf_nodes(node.left))
        if node.right:
            result.extend(self._leaf_nodes(node.right))

        return result

    def print(self, node, level=0):
        if node is not None:
            self.print(node.left, level + 1)
            print(' ' * 4 * level + '->', node.value)
            self.print(node.right, level + 1)

    def to_string(self, node):
        return str(self._as_list(node))

    def as_list(self):
        return self._as_list(self.root)

    def _as_list(self, node):
        result = []
        if node is not None:
            if type(node.value) == list:
                result.append(self._as_list(node.left))
                result.append(self._as_list(node.right))
            else:
                return node.value
            return result
        return []


class Node(object):

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def is_leaf(self):
        return self.left is None and self.right is None


def get_left_number_node(tree, node):
    leaf_nodes = tree.leaf_nodes()
    target_node = node.left if type(node.left.value) == int else node.right
    if type(target_node.value) != int:
        return None

    node_index = leaf_nodes.index(target_node)
    if node_index > 0:
        return leaf_nodes[node_index - 1]


def get_right_number_node(tree, node):
    leaf_nodes = tree.leaf_nodes()
    target_node = node.right if type(node.right.value) == int else node.left
    if type(target_node.value) != int:
        return None

    node_index = leaf_nodes.index(target_node)
    if node_index < len(leaf_nodes) - 1:
        return leaf_nodes[node_index + 1]


def explode(tree, node):
    left_number_node = get_left_number_node(tree, node)
    if left_number_node:
        left_number_node.value += node.left.value

    right_number_node = get_right_number_node(tree, node)
    if right_number_node:
        right_number_node.value += node.right.value

    node.value = 0
    node.left = node.right = None


def scan_for_explodes(tree):
    for node in tree.nodes():
        if type(node.value) == list:
            if tree.distance_to_root(node) > 4:
                explode(tree, node)
                return True
    return False


def split(node):
    left_value = node.value // 2
    right_value = math.ceil(node.value / 2)
    node.value = [left_value, right_value]
    node.left = Node(left_value)
    node.right = Node(right_value)


def scan_for_splits(tree):
    for node in tree.nodes():
        if type(node.value) == int:
            if node.value >= 10:
                split(node)
                return True
    return False


def reduce(tree):
    while True:
        if scan_for_explodes(tree):
            continue
        if scan_for_splits(tree):
            continue
        break


def add(tree, sfn):
    new_root = Node([tree.as_list(), sfn])
    new_root.left = tree.root
    new_root.right = Tree.from_list(sfn).root

    tree.root = new_root

    reduce(tree)


def _magnitude(tree, node):
    if node is None:
        return 0
    if type(node.value) == int:
        return node.value
    return 3 * (_magnitude(tree, node.left)) + (2 * _magnitude(tree, node.right))


def magnitude(tree):
    return _magnitude(tree, tree.root)


def do_run(tree, data):
    for sfn in data:
        add(tree, sfn)


def elapsed_time(start_time: int, end_time: int) -> str:
    t = end_time - start_time
    unit = 'seconds'
    if t < 1:
        t = t * 1000
        unit = 'milliseconds'
    if t < 1:
        t = t * 1000
        unit = 'microseconds'
    if t < 1:
        t = t * 1000
        unit = 'nanoseconds'

    return f'{t:.2f} {unit}'


def init_data():
    data = []
    with open('data.txt', 'r') as data_file:
        lines = data_file.read().splitlines()
    for line in lines:
        data.append(ast.literal_eval(line))
    return data


def main() -> None:
    data = init_data()
    tree = Tree.from_list(data[0])

    start_time = time.perf_counter()
    do_run(tree, data[1:])
    end_time = time.perf_counter()
    print(f'\nPart 1, magnitude: {magnitude(tree)}')
    print(f'Elapsed time: {elapsed_time(start_time, end_time)}')

    start_time = time.perf_counter()
    max_magnitude = 0
    for sfn1, sfn2 in itertools.permutations(data, 2):
        s1 = Tree.from_list(sfn1)
        add(s1, sfn2)
        m = magnitude(s1)
        if m > max_magnitude:
            max_magnitude = m
    end_time = time.perf_counter()

    print(f'\nPart 2, max_magnitude = {max_magnitude}')
    print(f'Elapsed time: {elapsed_time(start_time, end_time)}')


if __name__ == '__main__':
    main()
