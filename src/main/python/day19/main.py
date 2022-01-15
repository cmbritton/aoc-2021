import time

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from time import sleep
from mpl_toolkits.mplot3d import Axes3D
import re
import itertools as it
from collections import namedtuple
import copy
import cProfile

ROTATION_MATRICES = (
    (
        (1, 0, 0),
        (0, 0, -1),
        (0, 1, 0)
    ),
    (
        (1, 0, 0),
        (0, -1, 0),
        (0, 0, -1)
    ),
    (
        (1, 0, 0),
        (0, 0, 1),
        (0, -1, 0)
    ),
    (
        (0, 0, 1),
        (0, 1, 0),
        (-1, 0, 0)
    ),
    (
        (-1, 0, 0),
        (0, 1, 0),
        (0, 0, -1)
    ),
    (
        (0, 0, -1),
        (0, 1, 0),
        (1, 0, 0)
    ),
    (
        (0, -1, 0),
        (1, 0, 0),
        (0, 0, 1)
    ),
    (
        (-1, 0, 0),
        (0, -1, 0),
        (0, 0, 1)
    ),
    (
        (0, 1, 0),
        (-1, 0, 0),
        (0, 0, 1)
    ),
    (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1)
    ),
    (
        (0, 0, 1),
        (1, 0, 0),
        (0, 1, 0)
    ),
    (
        (-1, 0, 0),
        (0, 0, 1),
        (0, 1, 0)
    ),
    (
        (0, 0, -1),
        (-1, 0, 0),
        (0, 1, 0)
    ),
    (
        (0, -1, 0),
        (0, 0, -1),
        (1, 0, 0)
    ),
    (
        (-1, 0, 0),
        (0, 0, -1),
        (0, -1, 0)
    ),
    (
        (0, 1, 0),
        (0, 0, -1),
        (-1, 0, 0)
    ),
    (
        (0, 0, 1),
        (0, -1, 0),
        (1, 0, 0)
    ),
    (
        (0, 0, -1),
        (0, -1, 0),
        (-1, 0, 0)
    ),
    (
        (0, -1, 0),
        (-1, 0, 0),
        (0, 0, -1)
    ),
    (
        (0, 1, 0),
        (1, 0, 0),
        (0, 0, -1)
    ),
    (
        (0, 0, 1),
        (-1, 0, 0),
        (0, -1, 0)
    ),
    (
        (0, 0, -1),
        (1, 0, 0),
        (0, -1, 0)
    ),
    (
        (0, -1, 0),
        (0, 0, 1),
        (-1, 0, 0)
    ),
    (
        (0, 1, 0),
        (0, 0, 1),
        (1, 0, 0)
    )
)


class Scanner(object):
    MIN_COMMON_BEACONS = 12

    def __init__(self, name: str, beacons: list) -> object:
        self.name = name
        self.beacons = beacons
        self.rotation_matrix = None
        self.common_indexes = {}
        self.origin_position = None

    def is_oriented(self) -> bool:
        return self.rotation_matrix is not None

    def rotate(self, rotation_matrix: tuple) -> object:
        rotated_beacons = list(
            [np.dot(rotation_matrix, np.array(p, dtype=tuple)) for p in
             self.beacons])
        rotated_beacons = [(x, y, z) for x, y, z in rotated_beacons]

        rotated_scanner = Scanner(self.name, rotated_beacons)
        rotated_scanner.rotation_matrix = rotation_matrix
        rotated_scanner.common_indexes = self.common_indexes
        rotated_scanner.origin_position = self.origin_position
        return rotated_scanner

    def translate(self, beacon: tuple) -> tuple:
        return (beacon[0] + self.origin_position[0],
                beacon[1] + self.origin_position[1],
                beacon[2] + self.origin_position[2])

    def compute_common_beacons(self, other: object) -> int:
        common_indexes_self = []
        common_indexes_other = []
        for b1_self, b2_self in it.permutations(self.beacons, r=2):
            for b1_other, b2_other in it.permutations(other.beacons, r=2):
                if ((b1_self[0] - b2_self[0]) - (b1_other[0] - b2_other[0])) == 0 and \
                        ((b1_self[1] - b2_self[1]) - (b1_other[1] - b2_other[1])) == 0 and \
                        ((b1_self[2] - b2_self[2]) - (b1_other[2] - b2_other[2])) == 0:
                    idx = self.beacons.index(b1_self)
                    if idx not in common_indexes_self:
                        common_indexes_self.append(self.beacons.index(b1_self))

                    idx = self.beacons.index(b2_self)
                    if idx not in common_indexes_self:
                        common_indexes_self.append(self.beacons.index(b2_self))

                    idx = other.beacons.index(b1_other)
                    if idx not in common_indexes_other:
                        common_indexes_other.append(other.beacons.index(b1_other))

                    idx = other.beacons.index(b2_other)
                    if idx not in common_indexes_other:
                        common_indexes_other.append(other.beacons.index(b2_other))

                    if len(common_indexes_self) >= Scanner.MIN_COMMON_BEACONS:
                        if len(common_indexes_other) >= Scanner.MIN_COMMON_BEACONS:
                            break
            if len(common_indexes_self) >= Scanner.MIN_COMMON_BEACONS:
                if len(common_indexes_other) >= Scanner.MIN_COMMON_BEACONS:
                    break

        if len(common_indexes_self) >= Scanner.MIN_COMMON_BEACONS:
            self.common_indexes[other.name] = common_indexes_self

        if len(common_indexes_other) >= Scanner.MIN_COMMON_BEACONS:
            other.common_indexes[self.name] = common_indexes_other

        return len(common_indexes_self)


class Simulator(object):

    def __init__(self):
        self.scanners = None

    @staticmethod
    def find_overlaps(s1: Scanner, s2: Scanner) -> int:
        overlap_count = 0
        for rotation_matrix in ROTATION_MATRICES:
            rs2 = s2.rotate(rotation_matrix)
            overlaps = s1.compute_common_beacons(rs2)
            if overlaps > overlap_count:
                overlap_count = overlaps
                if overlaps >= Scanner.MIN_COMMON_BEACONS:
                    s2.rotation_matrix = rotation_matrix
                    s2.beacons = rs2.beacons
                    s2.common_indexes = rs2.common_indexes
                    s1_common_index = s1.common_indexes[s2.name][0]
                    s2_common_index = s2.common_indexes[s1.name][0]
                    s2.origin_position = (
                        s1.origin_position[0] - (rs2.beacons[s2_common_index][0] - s1.beacons[s1_common_index][0]),
                        s1.origin_position[1] - (rs2.beacons[s2_common_index][1] - s1.beacons[s1_common_index][1]),
                        s1.origin_position[2] - (rs2.beacons[s2_common_index][2] - s1.beacons[s1_common_index][2])
                    )
                    break
        return overlap_count

    def init_data(self) -> None:
        self.scanners = {}
        with open('../../resources/day19.data', 'r') as data_file:
            data_lines = data_file.readlines()
        scanner_name = None
        beacons = None
        for line in data_lines:
            line = line.strip()
            if line.startswith('---'):
                if beacons:
                    self.scanners[scanner_name] = Scanner(scanner_name, beacons)
                beacons = []
                m = re.search(r'--- ([^-]+) ---', line)
                scanner_name = m.group(1)
                continue
            if line:
                m = re.search(r'([-0-9]*),([-0-9]*),([-0-9]*)', line)
                beacons.append((int(m.group(1)),
                                int(m.group(2)),
                                int(m.group(3))))
        self.scanners[scanner_name] = Scanner(scanner_name, beacons)
        scanner = self.scanners['scanner 0']
        scanner.origin_position = (0, 0, 0)
        scanner.rotation_matrix = ((1, 0, 0), (0, 1, 0), (0, 0, 1))

    def done(self, pbar: object) -> bool:
        scanners_done = 0
        done = True
        for scanner in self.scanners.values():
            if scanner.is_oriented():
                scanners_done += 1
            else:
                done = False

        pbar.n = int((scanners_done / len(self.scanners)) * 100)
        pbar.refresh()
        return done

    def find_overlapping_beacons(self) -> None:
        pbar = tqdm(total=100)
        while not self.done(pbar):
            for s1_name, s2_name in it.combinations(self.scanners.keys(), r=2):
                s1 = self.scanners[s1_name]
                s2 = self.scanners[s2_name]
                if not s1.is_oriented() and s2.is_oriented():
                    s1, s2 = s2, s1
                if s1.is_oriented() and not s2.is_oriented():
                    self.find_overlaps(s1, s2)

    def run(self) -> None:
        self.init_data()
        self.find_overlapping_beacons()
        beacons = set()
        for scanner_name in self.scanners:
            for beacon in self.scanners[scanner_name].beacons:
                if self.scanners[scanner_name].origin_position is not None:
                    if self.scanners[scanner_name].rotation_matrix is not None:
                        beacons.add(self.scanners[scanner_name].translate(beacon))
        print(f'beacon count = {len(beacons)}')

        return


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


def main() -> None:
    start_time = time.time()
    simulator = Simulator()
    # cProfile.runctx('simulator.run()', globals(), locals())
    simulator.run()
    end_time = time.time()
    print(f'elapsed time = {elapsed_time(start_time, end_time)}')

    # ax = plt.axes(projection='3d')
    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.set_zlabel('Z')
    # ax.set_xlim3d(0, 5)
    # ax.set_ylim3d(0, 5)
    # ax.set_zlim3d(0, 5)

    # points = np.array([[[3, 2]], [[3, 2]], [[3, 2]]])

    # x_values = np.array([3], dtype=int)
    # y_values = np.array([3], dtype=int)
    # z_values = np.array([3], dtype=int)
    # fig = plt.figure(figsize=(5, 5))
    # ax.scatter3D(x_values, y_values, z_values, c='red', marker='o')

    # ax.scatter3D(points[0, :], points[1, :], points[2, :], c='red', marker='o')

    # x2_values = np.array([354, 467], dtype=int)
    # y2_values = np.array([478, 821], dtype=int)
    # z2_values = np.array([111, 399], dtype=int)
    # fig = plt.figure(figsize=(5, 5))

    # points2 = np.rot90(points, k=1, axes=(0, 1))
    # ax.scatter3D(points2[0, :], points2[1, :], points2[2, :], c='blue', marker='^')

    # ax.scatter(x_values, y_values, z_values, zdir='z', c='red')
    # plt.grid(True)
    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1, projection='3d')
    # ax.scatter(2, 2, 2, zdir='z', c='red')
    # y_values = [3, 4, 5]
    # plt.plot(x_values, y_values, color='blue', linewidth=2.5, linestyle='',
    #          marker='o')

    # plt.show()


if __name__ == '__main__':
    main()
