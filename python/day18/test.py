import unittest
from main import get_left_number_node, get_right_number_node, Tree, Node, scan_for_explodes, scan_for_splits
from main import magnitude, add

test_get_left_number_data = [
    {'sfn': [[[[[9, 8], 1], 2], 3], 4], 'coord': [9, 8], 'expected_result': None},
    {'sfn': [[[[[9, 8], [7, 3]], 2], 3], 4], 'coord': [9, 8], 'expected_result': None},
    {'sfn': [7, [6, [5, [4, [3, 2]]]]], 'coord': [3, 2], 'expected_result': 4},
    {'sfn': [[6, [5, [4, [3, 2]]]], 1], 'coord': [3, 2], 'expected_result': 4},
    {'sfn': [[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]], 'coord': [7, 3], 'expected_result': 1},
]

test_get_right_number_data = [
    {'sfn': [[[[[9, 8], 1], 2], 3], 4], 'coord': [9, 8], 'expected_result': 1},
    {'sfn': [[[[[9, 8], [7, 3]], 2], 3], 4], 'coord': [9, 8], 'expected_result': 7},
    {'sfn': [7, [6, [5, [4, [3, 2]]]]], 'coord': [3, 2], 'expected_result': None},
    {'sfn': [[6, [5, [4, [3, 2]]]], 1], 'coord': [3, 2], 'expected_result': 1},
    {'sfn': [[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]], 'coord': [7, 3], 'expected_result': 6}
]

test_explode_data = [
    {'sfn': [[[[[9, 8], 1], 2], 3], 4], 'expected_result': [[[[0, 9], 2], 3], 4]},
    {'sfn': [[[[[9, 8], [7, 3]], 2], 3], 4], 'expected_result': [[[[0, [15, 3]], 2], 3], 4]},
    {'sfn': [7, [6, [5, [4, [3, 2]]]]], 'expected_result': [7, [6, [5, [7, 0]]]]},
    {'sfn': [[6, [5, [4, [3, 2]]]], 1], 'expected_result': [[6, [5, [7, 0]]], 3]},
    {'sfn': [[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]],
     'expected_result': [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]}
]

test_split_data = [
    {'sfn': [[[[0, 7], 4], [15, [0, 13]]], [1, 1]], 'expected_result': [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]},
    {'sfn': [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]],
     'expected_result': [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]}
]

test_add_data = [
    {
        'sfn1': [[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]],
        'sfn2': [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]],
        'expected_result': [[[[4, 0], [5, 4]], [[7, 7], [6, 0]]], [[8, [7, 7]], [[7, 9], [5, 0]]]]
    },
    {
        'sfn1': [[[[4, 0], [5, 4]], [[7, 7], [6, 0]]], [[8, [7, 7]], [[7, 9], [5, 0]]]],
        'sfn2': [[2, [[0, 8], [3, 4]]], [[[6, 7], 1], [7, [1, 6]]]],
        'expected_result': [[[[6, 7], [6, 7]], [[7, 7], [0, 7]]], [[[8, 7], [7, 7]], [[8, 8], [8, 0]]]]
    },
    {
        'sfn1': [[[[6, 7], [6, 7]], [[7, 7], [0, 7]]], [[[8, 7], [7, 7]], [[8, 8], [8, 0]]]],
        'sfn2': [[[[2, 4], 7], [6, [0, 5]]], [[[6, 8], [2, 8]], [[2, 1], [4, 5]]]],
        'expected_result': [[[[7, 0], [7, 7]], [[7, 7], [7, 8]]], [[[7, 7], [8, 8]], [[7, 7], [8, 7]]]]
    },
    {
        'sfn1': [[[[7, 0], [7, 7]], [[7, 7], [7, 8]]], [[[7, 7], [8, 8]], [[7, 7], [8, 7]]]],
        'sfn2': [7, [5, [[3, 8], [1, 4]]]],
        'expected_result': [[[[7, 7], [7, 8]], [[9, 5], [8, 7]]], [[[6, 8], [0, 8]], [[9, 9], [9, 0]]]]
    },
    {
        'sfn1': [[[[7, 7], [7, 8]], [[9, 5], [8, 7]]], [[[6, 8], [0, 8]], [[9, 9], [9, 0]]]],
        'sfn2': [[2, [2, 2]], [8, [8, 1]]],
        'expected_result': [[[[6, 6], [6, 6]], [[6, 0], [6, 7]]], [[[7, 7], [8, 9]], [8, [8, 1]]]]
    },
    {
        'sfn1': [[[[6, 6], [6, 6]], [[6, 0], [6, 7]]], [[[7, 7], [8, 9]], [8, [8, 1]]]],
        'sfn2': [2, 9],
        'expected_result': [[[[6, 6], [7, 7]], [[0, 7], [7, 7]]], [[[5, 5], [5, 6]], 9]]
    },
    {
        'sfn1': [[[[6, 6], [7, 7]], [[0, 7], [7, 7]]], [[[5, 5], [5, 6]], 9]],
        'sfn2': [1, [[[9, 3], 9], [[9, 0], [0, 7]]]],
        'expected_result': [[[[7, 8], [6, 7]], [[6, 8], [0, 8]]], [[[7, 7], [5, 0]], [[5, 5], [5, 6]]]]
    },
    {
        'sfn1': [[[[7, 8], [6, 7]], [[6, 8], [0, 8]]], [[[7, 7], [5, 0]], [[5, 5], [5, 6]]]],
        'sfn2': [[[5, [7, 4]], 7], 1],
        'expected_result': [[[[7, 7], [7, 7]], [[8, 7], [8, 7]]], [[[7, 0], [7, 7]], 9]]
    },
    {
        'sfn1': [[[[7, 7], [7, 7]], [[8, 7], [8, 7]]], [[[7, 0], [7, 7]], 9]],
        'sfn2': [[[[4, 2], 2], 6], [8, 7]],
        'expected_result': [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
    }
]

test_magnitude_data = [
    {'sfn': [[1, 2], [[3, 4], 5]], 'expected_result': 143},
    {'sfn': [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]], 'expected_result': 1384},
    {'sfn': [[[[1, 1], [2, 2]], [3, 3]], [4, 4]], 'expected_result': 445},
    {'sfn': [[[[3, 0], [5, 3]], [4, 4]], [5, 5]], 'expected_result': 791},
    {'sfn': [[[[5, 0], [7, 4]], [5, 5]], [6, 6]], 'expected_result': 1137},
    {'sfn': [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]], 'expected_result': 3488},
]


class MyTestCase(unittest.TestCase):
    def test_get_left_number(self):
        for data in test_get_left_number_data:
            tree = Tree.from_list(data['sfn'])
            node = tree.find_node(tree.root, data['coord'])
            left_number_node = get_left_number_node(tree, node)
            if data['expected_result']:
                self.assertEqual(data['expected_result'], left_number_node.value, 'test_get_left_number')
            else:
                self.assertEqual(data['expected_result'], left_number_node, 'test_get_left_number')

    def test_get_right_number(self):
        for data in test_get_right_number_data:
            tree = Tree.from_list(data['sfn'])
            node = tree.find_node(tree.root, data['coord'])
            right_number_node = get_right_number_node(tree, node)
            if data['expected_result']:
                self.assertEqual(data['expected_result'], right_number_node.value, 'test_get_right_number')
            else:
                self.assertEqual(data['expected_result'], right_number_node, 'test_get_right_number')

    def test_explode(self):
        for data in test_explode_data:
            tree = Tree.from_list(data['sfn'])
            scan_for_explodes(tree)
            result = tree.as_list()
            self.assertEqual(data['expected_result'], result, 'test_explode')

    def test_split(self):
        for data in test_split_data:
            tree = Tree.from_list(data['sfn'])
            scan_for_splits(tree)
            result = tree.as_list()
            self.assertEqual(data['expected_result'], result, 'test_split')

    def test_add(self):
        for data in test_add_data:
            tree = Tree.from_list(data['sfn1'])
            add(tree, data['sfn2'])
            result = tree.as_list()
            self.assertEqual(data['expected_result'], result, 'test_add')

    def test_magnitude(self):
        for data in test_magnitude_data:
            tree = Tree.from_list(data['sfn'])
            result = magnitude(tree)
            self.assertEqual(data['expected_result'], result, 'test_magnitude')


if __name__ == '__main__':
    unittest.main()
