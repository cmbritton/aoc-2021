import re
from typing import Tuple
import time


def is_target_boundary_exceeded(point, target_dim):
    return point[0] > target_dim[1] or point[1] < target_dim[2]


def is_in_target_area(point, target_dim):
    return (target_dim[0] <= point[0] <= target_dim[1]) and (target_dim[2] <= point[1] <= target_dim[3])


def step(x, y, delta_x, delta_y):
    x += delta_x
    if delta_x:
        delta_x -= 1
    y += delta_y
    delta_y -= 1
    return x, y, delta_x, delta_y


def simulate(start_velocity, target_dim):
    path = []
    current_x = 0
    delta_x = start_velocity[0]
    current_y = 0
    delta_y = start_velocity[1]
    while not is_target_boundary_exceeded((current_x, current_y), target_dim):
        current_x, current_y, delta_x, delta_y = step(current_x, current_y, delta_x, delta_y)
        path.append((current_x, current_y))
        if is_in_target_area((current_x, current_y), target_dim):
            return path
    return None


def highest_y_path(valid_paths):
    best_start_velocity = None
    best_path = None
    max_y = -999999
    for start_velocity, path in valid_paths.items():
        for value in path:
            if value[1] > max_y:
                max_y = value[1]
                best_start_velocity = start_velocity
                best_path = path
    return best_start_velocity, best_path, max_y


def end_x(start_x):
    value = 0
    while start_x > 0:
        value += start_x
        start_x -= 1
    return value


def get_min_start_x(target_dim):
    start_x = 0
    while end_x(start_x) < target_dim[0]:
        start_x += 1
    return start_x


def do_run(target_dim):
    valid_paths = {}
    for x in range(get_min_start_x(target_dim), target_dim[1] + 1):
        for y in range(500, target_dim[2] - 1, -1):
            path = simulate((x, y), target_dim)
            if path:
                valid_paths[(x, y)] = path

    return valid_paths


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
    with open('../../data/day17.data', 'r') as data_file:
        line = data_file.readline()
    m = re.search(r'target area: x=([-0-9]*)\.\.([-0-9]*), y=([-0-9]*)\.\.([-0-9]*)', line)
    return int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))


def main() -> None:
    target_dim = init_data()

    start_time = time.perf_counter()
    valid_paths = do_run(target_dim)
    best_start_velocity, best_path, max_y = highest_y_path(valid_paths)
    end_time = time.perf_counter()
    print(f'\nPart 1, highest y: {max_y}')
    print(f'Part 2, Total valid paths = {len(valid_paths)}')
    print(f'Elapsed time: {elapsed_time(start_time, end_time)}')


if __name__ == '__main__':
    main()
