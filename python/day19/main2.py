import itertools as it
import time

import numpy as np
import re


MINIMUM_BEACON_OVERLAPS = 12

ROTATION_MATRICES = np.array((
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
))


def overlaps(oriented_scanner, origin, rotated_scanner):
    overlap_count = 0
    oriented_beacon_pairs = np.array(list(it.permutations(oriented_scanner, r=2)), dtype=int)
    rotated_beacon_pairs = np.array(list(it.permutations(rotated_scanner, r=2)), dtype=int)
    oriented_start_beacons = np.array([a[0] for a in oriented_beacon_pairs])
    oriented_end_beacons = np.array([a[1] for a in oriented_beacon_pairs])
    rotated_start_beacons = np.array([a[0] for a in rotated_beacon_pairs])
    rotated_end_beacons = np.array([a[1] for a in rotated_beacon_pairs])
    # beacon_pairs = np.array([[x, y] for x in np.array(list(it.permutations(oriented_beacon_pairs, r=2))) for y in np.array(list(it.permutations(rotated_beacon_pairs, r=2)))])
    matching_pairs = []
    for oriented_beacon_pair in oriented_beacon_pairs:
        for rotated_beacon_pair in rotated_beacon_pairs:
            oriented_diff = oriented_beacon_pair[0] - oriented_beacon_pair[1]
            rotated_diff = rotated_beacon_pair[0] - rotated_beacon_pair[1]
            if not any(oriented_diff - rotated_diff):
                overlap_count += 1
                matching_pairs.append((oriented_beacon_pair, rotated_beacon_pair))
                if overlap_count >= MINIMUM_BEACON_OVERLAPS:
                    # print(f'\n{str(matching_pairs)}')
                    new_origin = (origin[0] + (oriented_beacon_pair[0][0] - rotated_beacon_pair[0][0]),
                                  origin[1] + (oriented_beacon_pair[0][1] - rotated_beacon_pair[0][1]),
                                  origin[2] + (oriented_beacon_pair[0][2] - rotated_beacon_pair[0][2]))
                    scanner = translate(rotated_scanner, new_origin)
                    return scanner, new_origin
    return None, None


def translate(scanner, translation):
    translated_scanner = []
    for beacon in scanner:
        translated_scanner.append((beacon[0] + translation[0], beacon[1] + translation[1], beacon[2] + translation[2]))
    return translated_scanner


def rotate_beacon(beacon, rotation_matrix):
    result = np.dot(rotation_matrix, beacon)
    return result


def rotate_scanner(unrotated_scanner, rotation_matrix):
    rotated_scanner = [rotate_beacon(beacon, rotation_matrix)
                       for beacon, rotation_matrix in it.product(unrotated_scanner, [rotation_matrix])]
    return rotated_scanner


def elapsed_time(start_time: float, end_time: float) -> str:
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


with open('../../data/day19.data', 'r') as data_file:
    data_lines = data_file.readlines()
unoriented_scanners = []
beacons = None
for line in data_lines:
    line = line.strip()
    if line.startswith('---'):
        if beacons is not None:
            unoriented_scanners.append(beacons)
        beacons = []
        m = re.search(r'--- ([^-]+) ---', line)
        continue
    if line:
        m = re.search(r'([-0-9]*),([-0-9]*),([-0-9]*)', line)
        beacon = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        beacons.append(beacon)

unoriented_scanners.append(beacons)

origins = [(0, 0, 0)]

oriented_scanners = [unoriented_scanners[0]]
unoriented_scanners = unoriented_scanners[1:]

rotations = [((1, 0, 0), (0, 1, 0), (0, 0, 1))]

beacons = data_lines = line = m = beacon = data_file = None

start_time = time.time()

while len(unoriented_scanners) > 0:
    unoriented_scanner = unoriented_scanners.pop()
    found = False
    for i, oriented_scanner in enumerate(oriented_scanners):
        origin = origins[i]
        for rotation_matrix in ROTATION_MATRICES:
            rotated_scanner = rotate_scanner(unoriented_scanner, rotation_matrix)
            scanner, new_origin = overlaps(oriented_scanner, origin, rotated_scanner)
            if scanner is not None:
                oriented_scanners.append(scanner)
                origins.append(new_origin)
                found = True
                break
        if found:
            break
    if not found:
        unoriented_scanners.insert(0, unoriented_scanner)

beacons = set()
for scanner in oriented_scanners:
    for beacon in scanner:
        beacons.add(tuple(beacon))

end_time = time.time()
print(f'elapsed time = {elapsed_time(start_time, end_time)}')

print(f'Part 1, beacons = {len(beacons)}')
