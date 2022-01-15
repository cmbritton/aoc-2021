from main import main


class Position(object):

    def __init__(self):
        self.horizontal = self.depth = 0


class Submarine(object):

    def __init__(self):
        self.position = Position()

    def move(self, direction, units):
        if direction == 'forward':
            self.position.horizontal += units
        elif direction == 'down':
            self.position.depth += units
        elif direction == 'up':
            self.position.depth -= units


main(Submarine())
