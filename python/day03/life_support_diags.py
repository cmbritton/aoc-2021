class LifeSupportDiagnostics(object):
    BITS_PER_VALUE = 12

    def __init__(self):
        self.values = []

    def o2_rating(self):
        o2_values = self.values.copy()
        return self.reduce_values(o2_values, self.most_common_value)

    def co2_rating(self):
        co2_values = self.values.copy()
        return self.reduce_values(co2_values, self.least_common_value)

    def reduce_values(self, values, bit_criteria_function):
        for position in range(LifeSupportDiagnostics.BITS_PER_VALUE):
            self.discard_values(values, position, bit_criteria_function)
            if len(values) == 1:
                return values[0]

    def discard_values(self, values, position, bit_criteria_function):
        index = 0
        bit_value = bit_criteria_function(values, position)
        while index < len(values):
            if self.get_bit_value(values[index], position) != bit_value:
                del values[index]
            else:
                index += 1

    def get_bit_value(self, value, position):
        return (value >> LifeSupportDiagnostics.BITS_PER_VALUE - position - 1) & 1

    def position_counts(self, values, position):
        counts = [0] * 2
        for value in values:
            counts[self.get_bit_value(value, position)] += 1
        return counts

    def most_common_value(self, values, position):
        [zero_count, one_count] = self.position_counts(values, position)
        return 1 if one_count >= zero_count else 0

    def least_common_value(self, values, position):
        [zero_count, one_count] = self.position_counts(values, position)
        return 0 if zero_count <= one_count else 1

    def rating(self):
        return self.o2_rating() * self.co2_rating()


def main():
    life_support_diagnostics = LifeSupportDiagnostics()
    with open('../../data/day03.data', 'r') as data_file:
        line = data_file.readline()
        while line:
            life_support_diagnostics.values.append(int(line.strip(), 2))
            line = data_file.readline()
    print("value: {}".format(life_support_diagnostics.rating()))


main()
