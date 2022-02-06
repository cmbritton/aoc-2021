import os
import psutil

import numpy as np
from scipy.signal import convolve2d

# This is not my code. I copied it from https://github.com/fuglede/adventofcode/blob/master/2021/day20/solutions.py
# to study.

with open("../../data/day20.data") as f:
    ls = f.read().strip().split("\n")

enhancement = np.array(list(ls[0])) == "#"
grid = np.array(list(map(list, ls[2:]))) == "#"
kernel = 2 ** np.arange(9).reshape((3, 3))

for i in range(50):
    grid = enhancement[convolve2d(grid, kernel, fillvalue=i % 2)]
    if i in (1, 49):
        print(grid.sum())

process = psutil.Process(os.getpid())
print(process.memory_info().rss)  # in bytes
