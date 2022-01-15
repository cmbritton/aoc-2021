class Graph(object):

    def __init__(self) -> None:
        self.nodes = set()
        self.edges = {}

    def add_node(self, node) -> None:
        self.nodes.add(node)
        if node not in self.edges:
            self.edges[node] = []

    def add_edge(self, from_node, to_node) -> None:
        self.add_node(from_node)
        self.add_node(to_node)
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)

    @staticmethod
    def is_any_small_node_in_path_twice(path) -> bool:
        nodes_in_path = []
        for node in path:
            if node.islower():
                if node in nodes_in_path:
                    return True
                else:
                    nodes_in_path.append(node)
        return False

    def can_add_small_node(self, node, path, is_part_2) -> bool:
        if node.islower() and node in path:
            if is_part_2 and node != 'start':
                if self.is_any_small_node_in_path_twice(path):
                    return False
            else:
                return False
        return True

    def get_all_paths(self, g, start, end, path, completed_paths, is_part_2) -> (list, list):
        if not self.can_add_small_node(start, path, is_part_2):
            return path, completed_paths
        path.append(start)
        if start == end:
            completed_paths.append(path.copy())
        else:
            for child_node in g.edges[start]:
                if self.can_add_small_node(child_node, path, is_part_2) or child_node.isupper():
                    self.get_all_paths(g, child_node, end, path, completed_paths, is_part_2)
        path.pop()
        return path, completed_paths


def build_graph() -> Graph:
    g = Graph()
    with open('../../data/day12.data', 'r') as data_file:
        lines = data_file.read().splitlines()
        for line in lines:
            from_node, to_node = line.split('-')
            g.add_edge(from_node, to_node)
    return g


def main() -> None:
    g = build_graph()
    path, paths = g.get_all_paths(g, 'start', 'end', [], [], is_part_2=False)
    print('Part 1, path_count = {}'.format(len(paths)))

    path, paths = g.get_all_paths(g, 'start', 'end', [], [], is_part_2=True)
    print('Part 2, path_count = {}'.format(len(paths)))


main()
