def main(submarine):
    with open('sub_position.data', 'r') as data_file:
        line = data_file.readline()
        while line:
            [direction, units] = line.strip().split()
            submarine.move(direction=direction, units=int(units))
            line = data_file.readline()
    print("horizontal * depth = {}".format(submarine.position.horizontal * submarine.position.depth))
