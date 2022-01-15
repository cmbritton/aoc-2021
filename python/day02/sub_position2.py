from main import main


class Position(object):

    def __init__(self):
        self.horizontal = self.depth = self.aim = 0


class Submarine(object):

    def __init__(self):
        self.position = Position()

    def move(self, direction, units):
        if direction == 'forward':
            self.position.horizontal += units
            self.position.depth += self.position.aim * units
        elif direction == 'down':
            self.position.aim += units
        elif direction == 'up':
            self.position.aim -= units
        else:
            print("Unknown direction {}".format(direction))


main(Submarine())
