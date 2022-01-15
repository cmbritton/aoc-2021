import numpy


class Simulator(object):
    MAX_DAYS = 256
    SPAWN_CYCLE_DAYS = 7
    NEWBORN_SPAWN_DELAY_DAYS = 2
    AGE_BUCKET_SIZE = SPAWN_CYCLE_DAYS + NEWBORN_SPAWN_DELAY_DAYS + 1
    NEWBORN_CYCLE_DAYS = SPAWN_CYCLE_DAYS + NEWBORN_SPAWN_DELAY_DAYS

    def __init__(self, input_line):
        self.total_lantern_fish = 0
        init_ages_days = input_line.strip().split(',')
        self.generations = numpy.full(Simulator.AGE_BUCKET_SIZE, 0, dtype=numpy.uint)
        for i in range(len(init_ages_days)):
            self.generations[int(init_ages_days[i])] += 1
        self.day = 0

    def run(self):
        for day in range(Simulator.MAX_DAYS):
            self.tick()
            print('Total after {} days: {}'.format(self.day, numpy.sum(self.generations)))

    def tick(self):
        self.day += 1
        self.add_adolescents_to_adults()
        self.shift_young_generations()
        self.spawn()

    def spawn(self):
        spawn_index = (self.day - 1) % Simulator.SPAWN_CYCLE_DAYS
        self.generations[Simulator.NEWBORN_CYCLE_DAYS] = self.generations[spawn_index]

    def add_adolescents_to_adults(self):
        new_adult_index = (self.day - Simulator.NEWBORN_SPAWN_DELAY_DAYS) % Simulator.SPAWN_CYCLE_DAYS
        self.generations[new_adult_index] += self.generations[
            Simulator.NEWBORN_CYCLE_DAYS - Simulator.NEWBORN_SPAWN_DELAY_DAYS]

    def shift_young_generations(self):
        for i in range(Simulator.SPAWN_CYCLE_DAYS, Simulator.AGE_BUCKET_SIZE - 1):
            self.generations[i] = self.generations[i + 1]
        self.generations[Simulator.AGE_BUCKET_SIZE - 1] = 0


def main():
    with open('data.txt', 'r') as data_file:
        input_line = data_file.readline()
        simulator = Simulator(input_line)
        simulator.run()


main()
