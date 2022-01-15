import math
import numpy as np


low_point_indices = []


def is_lower(point):
    if adjacent_points_lower_than(point):
        low_point_indices.append(point)


def adjacent_points_lower_than(point):
    return all([is_lower_than_adjacent_points(point, adjacent_point) for adjacent_point in get_adjacent_points(point)])


def is_lower_than_adjacent_points(point, adjacent_point):
    return height_map[point] < height_map[adjacent_point]


def get_basin_points(point):
    points = set()
    points.update([point])
    y, x = point
    for adjacent_point in get_adjacent_points(point):
        adj_y, adj_x = adjacent_point
        if height_map[y][x] < height_map[adj_y][adj_x] < 9:
            points.update(get_basin_points(adjacent_point))
    return points


def get_adjacent_points(point):
    adjacent_points = set()
    y, x = point
    if y != 0:
        adjacent_points.update([(y - 1, x)])
    if x < index_map.shape[1] - 1:
        adjacent_points.update([(y, x + 1)])
    if y < index_map.shape[0] - 1:
        adjacent_points.update([(y + 1, x)])
    if x != 0:
        adjacent_points.update([(y, x - 1)])
    return adjacent_points


with open('data.txt', 'r') as data_file:
    lines = data_file.read().splitlines()

height_map = np.zeros((len(lines), len(lines[0])), dtype=np.ubyte)
index_map = np.zeros(np.shape(height_map), dtype=object)

for y in range(len(lines)):
    heights = list(lines[y])
    for x in range(len(heights)):
        height_map[y, x] = int(heights[x])
        index_map[y, x] = (y, x)

np.vectorize(is_lower)(index_map)
total_risk = sum(height_map[y][x] for y, x in low_point_indices) + len(low_point_indices)
print('Part 1, total_risk={}'.format(total_risk))

basin_sizes = []
for basin in [get_basin_points(point) for point in low_point_indices]:
    basin_sizes.append(len(basin))
top_sizes = sorted(basin_sizes, reverse=True)[:3]
print('Part 2, product of top 3 basin sizes: {}'.format(math.prod(top_sizes)))
