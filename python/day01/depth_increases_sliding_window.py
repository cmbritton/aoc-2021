# from _collections import deque
from collections import deque


class SlidingWindow(object):
    WINDOW_SIZE = 3

    def __init__(self):
        self.window = deque()
        self.input_values = open('../../data/day01.data', 'r')
        self.input_value = None

    def advance(self):
        input_line = self.input_values.readline()
        if not input_line:
            return False
        self.input_value = int(input_line.strip())
        self.window.append(self.input_value)
        if len(self.window) > SlidingWindow.WINDOW_SIZE:
            self.window.popleft()
        return True

    def is_full(self):
        return int(len(self.window)) == SlidingWindow.WINDOW_SIZE

    def total(self):
        total = 0
        for value in self.window:
            total += value
        return total

    def close(self):
        self.input_values.close()


def main():
    increase_count = 0
    prev_total = None
    sliding_window = SlidingWindow()
    while sliding_window.advance():
        if sliding_window.is_full():
            if prev_total is not None:
                if sliding_window.total() > prev_total:
                    increase_count += 1
            prev_total = sliding_window.total()
    sliding_window.close()
    print("increase_count: {}".format(increase_count))


main()
