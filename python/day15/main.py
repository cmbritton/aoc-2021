import timeit

import numpy as np


START_POINT = (0, 0)
END_POINT = None
INFINITY = 2 ** 32

risk_levels = accumulated_risk_levels = visited = shortest_path = None


def left(point) -> (int, int):
    if point is None:
        return None
    x, y = point
    if x > 0:
        return x - 1, y
    else:
        return None


def right(point) -> (int, int):
    if point is None:
        return None
    x, y = point
    if x < risk_levels.shape[1] - 1:
        return x + 1, y
    else:
        return None


def up(point) -> (int, int):
    if point is None:
        return None
    x, y = point
    if y > 0:
        return x, y - 1
    else:
        return None


def down(point) -> (int, int):
    if point is None:
        return None
    x, y = point
    if y < risk_levels.shape[0] - 1:
        return x, y + 1
    else:
        return None


def path_to_list() -> list:
    global risk_levels, shortest_path
    result = []
    current_node = END_POINT
    while current_node:
        result.append('{}:{}'.format(str(risk_levels[current_node]), current_node))
        current_node = shortest_path[current_node]
    result.reverse()
    return result


def path_to_string() -> str:
    global risk_levels, shortest_path
    return ' -> '.join(path_to_list())


def get_unvisited_lowest_cost_nodes() -> list:
    global visited, accumulated_risk_levels
    indexes = np.where(accumulated_risk_levels == np.min(np.ma.masked_where(visited, accumulated_risk_levels)))
    lowest_cost_points = []
    for i in range(len(indexes[0])):
        lowest_cost_points.append((indexes[0][i], indexes[1][i]))
    return lowest_cost_points


def get_unvisited_neighbors(current_node) -> list:
    global visited
    unvisited_neighbors = []
    for neighbor in [left(current_node), right(current_node), up(current_node), down(current_node)]:
        if neighbor and not visited[neighbor]:
            unvisited_neighbors.append(neighbor)
    return unvisited_neighbors


def calculate_lowest_risk() -> None:
    global visited, risk_levels, accumulated_risk_levels, shortest_path
    while np.count_nonzero(visited) < visited.size:
        lowest_cost_points = get_unvisited_lowest_cost_nodes()
        for current_node in lowest_cost_points:
            visited[current_node] = True
            unvisited_neighbors = get_unvisited_neighbors(current_node)

            if current_node == END_POINT:
                break
            for neighbor in unvisited_neighbors:
                neighbor_risk_level = accumulated_risk_levels[current_node] + risk_levels[neighbor]
                if neighbor_risk_level < accumulated_risk_levels[neighbor]:
                    accumulated_risk_levels[neighbor] = neighbor_risk_level
                    shortest_path[neighbor] = current_node
            if current_node == END_POINT or accumulated_risk_levels[current_node] == INFINITY or visited[END_POINT]:
                break


def expand_risk_level_along_axis(src_risk_level, axis_str, factor):
    axis = 1 if axis_str == 'x' else 0
    expansion_list = [src_risk_level]
    for i in range(factor - 1):
        tmp_expanded_risk_level = np.copy(src_risk_level)
        tmp_expanded_risk_level += 1 + i
        tmp_expanded_risk_level[tmp_expanded_risk_level > 9] = tmp_expanded_risk_level[tmp_expanded_risk_level > 9] % 9
        expansion_list.append(tmp_expanded_risk_level)
    return np.concatenate(tuple(expansion_list), axis=axis)


def expand_risk_levels():
    global risk_levels
    expand_factor_x = expand_factor_y = 5
    expanded_risk_levels = expand_risk_level_along_axis(risk_levels, 'x', expand_factor_x)
    return expand_risk_level_along_axis(expanded_risk_levels, 'y', expand_factor_y)


def setup_globals():
    global risk_levels, shortest_path, visited, accumulated_risk_levels, END_POINT
    shortest_path = np.zeros(risk_levels.shape, dtype=object)
    visited = np.zeros(risk_levels.shape, dtype=bool)
    accumulated_risk_levels = np.zeros(risk_levels.shape, dtype=int)
    accumulated_risk_levels = accumulated_risk_levels + INFINITY
    accumulated_risk_levels[START_POINT] = 0
    END_POINT = (risk_levels.shape[1] - 1, risk_levels.shape[0] - 1)


def print_results(part, elapsed_time_seconds):
    global accumulated_risk_levels
    print('\nPart {}, lowest risk: {}'.format(part, accumulated_risk_levels[END_POINT]))
    print('Elapsed time:        {} seconds'.format(elapsed_time_seconds))
    print('Path length:         {} hops'.format(len(path_to_list())))
    print('Path:                {}'.format(path_to_string()))


def init_data():
    with open('data.txt', 'r') as data_file:
        lines = data_file.read().splitlines()

    matrix = np.zeros((len(lines[0]), len(lines)), np.ubyte)

    for y in range(len(lines)):
        for x in range(len(lines[0])):
            matrix[x][y] = lines[y][x]  # Transpose rows and columns, so we can use x,y coordinates
    return matrix


def do_run(part):
    global risk_levels, accumulated_risk_levels, visited
    setup_globals()
    t = timeit.Timer(lambda: calculate_lowest_risk())
    elapsed_time_seconds = t.timeit(1)
    print_results(part, elapsed_time_seconds)


def main():
    global risk_levels
    risk_levels = init_data()
    setup_globals()
    do_run(1)

    risk_levels = expand_risk_levels()
    do_run(2)


if __name__ == '__main__':
    main()
