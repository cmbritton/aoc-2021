# Disclaimer. I am not at all proud of this code, but it works.
import itertools


class BadDigit(object):

    def __init__(self, bad_digit_value):
        self.value = ''.join(sorted(bad_digit_value))

    def get_good_value(self):
        if self.is_one():
            return '1'
        elif self.is_four():
            return '4'
        elif self.is_seven():
            return '7'
        elif self.is_eight():
            return '8'
        else:
            return '.'

    def is_one(self):
        return len(self.value) == 2

    def is_four(self):
        return len(self.value) == 4

    def is_seven(self):
        return len(self.value) == 3

    def is_eight(self):
        return len(self.value) == 7

    def is_zero_or_six(self):
        return len(self.value) == 6

    def is_two_three_five_or_nine(self):
        return len(self.value) == 5

    def to_string(self):
        return self.value

    def to_good_string(self):
        return self.get_good_value()


class BadDigitPattern(object):

    def __init__(self, bad_pattern):
        self.value = ''.join(sorted(bad_pattern))

    def is_one(self):
        return len(self.value) == 2

    def is_four(self):
        return len(self.value) == 4

    def is_seven(self):
        return len(self.value) == 3

    def is_eight(self):
        return len(self.value) == 7

    def is_zero_or_six(self):
        return len(self.value) == 6

    def is_two_three_five_or_nine(self):
        return len(self.value) == 5

    def to_string(self):
        return self.value


class SegmentDigit(object):
    ZERO = 'abcefg'
    ONE = 'cf'
    TWO = 'acdeg'
    THREE = 'acdfg'
    FOUR = 'bcdf'
    FIVE = 'abdfg'
    SIX = 'abdefg'
    SEVEN = 'acf'
    EIGHT = 'abcdefg'
    NINE = 'abcdfg'


class Entry(object):
    CROSS_CONNECTION_MAPS = list(itertools.permutations(['a', 'b', 'c', 'd', 'e', 'f', 'g']))

    def __init__(self, input_line):
        self.bad_digit_patterns = []
        self.bad_digit_values = []
        self.pattern_to_digit = dict()
        self.digit_to_pattern = dict()
        self.parse_input(input_line)
        self.map_index = self.find_valid_map()

    def find_valid_map(self):
        for i in range(len(Entry.CROSS_CONNECTION_MAPS)):
            if self.map_works(Entry.CROSS_CONNECTION_MAPS[i]):
                return i
        return -1

    def map_works(self, cross_connection_map):
        digits = []
        for bad_digit_pattern in self.bad_digit_patterns:
            digits.append(self.digit_from_pattern(bad_digit_pattern.value, cross_connection_map))
        if '0' in digits and '1' in digits and '2' in digits and '3' in digits and '4' in digits and '5' in digits \
                and '6' in digits and '7' in digits and '8' in digits and '9' in digits:
            return True
        return False

    def digit_from_pattern(self, bad_digit_pattern, cross_connection_map):
        if self.is_one(bad_digit_pattern):
            return '1'
        elif self.is_four(bad_digit_pattern):
            return '4'
        elif self.is_seven(bad_digit_pattern):
            return '7'
        elif self.is_eight(bad_digit_pattern):
            return '8'
        return self._make_digit_from_pattern(bad_digit_pattern, cross_connection_map)

    def _make_digit_from_pattern(self, bad_digit_pattern, cross_connection_map):
        translated_pattern = ''.join(sorted(self.translate_pattern(bad_digit_pattern, cross_connection_map)))
        if translated_pattern == SegmentDigit.ZERO:
            return '0'
        elif translated_pattern == SegmentDigit.TWO:
            return '2'
        elif translated_pattern == SegmentDigit.THREE:
            return '3'
        elif translated_pattern == SegmentDigit.FIVE:
            return '5'
        elif translated_pattern == SegmentDigit.SIX:
            return '6'
        elif translated_pattern == SegmentDigit.NINE:
            return '9'
        else:
            return '.'

    def translate_pattern(self, bad_digit_pattern, cross_connection_map):
        new_pattern = []
        for segment in bad_digit_pattern:
            new_pattern.append(cross_connection_map[self.segment_to_index(segment)])
        return ''.join(sorted(new_pattern))

    @staticmethod
    def segment_to_index(segment):
        if segment == 'a':
            return 0
        elif segment == 'b':
            return 1
        elif segment == 'c':
            return 2
        elif segment == 'd':
            return 3
        elif segment == 'e':
            return 4
        elif segment == 'f':
            return 5
        elif segment == 'g':
            return 6
        else:
            return -1

    @staticmethod
    def is_one(pattern):
        return len(pattern) == 2

    @staticmethod
    def is_four(pattern):
        return len(pattern) == 4

    @staticmethod
    def is_seven(pattern):
        return len(pattern) == 3

    @staticmethod
    def is_eight(pattern):
        return len(pattern) == 7

    @staticmethod
    def is_zero_six_or_nine(pattern):
        return len(pattern) == 6

    @staticmethod
    def is_two_three_five_or_nine(pattern):
        return len(pattern) == 5

    def parse_input(self, input_line):
        (bad_digit_patterns, bad_digit_values) = input_line.strip().split(' | ')
        self.parse_bad_digit_patterns(bad_digit_patterns)
        self.parse_bad_digit_values(bad_digit_values)

    def parse_bad_digit_patterns(self, bad_digit_patterns_str):
        for bad_digit_pattern_str in bad_digit_patterns_str.split(' '):
            bad_digit_pattern = BadDigitPattern(bad_digit_pattern_str)
            self.bad_digit_patterns.append(bad_digit_pattern)
            if bad_digit_pattern.is_one():
                self.pattern_to_digit[bad_digit_pattern] = '1'
                self.digit_to_pattern['1'] = bad_digit_pattern
            elif bad_digit_pattern.is_four():
                self.pattern_to_digit[bad_digit_pattern] = '4'
                self.digit_to_pattern['4'] = bad_digit_pattern
            elif bad_digit_pattern.is_seven():
                self.pattern_to_digit[bad_digit_pattern] = '7'
                self.digit_to_pattern['7'] = bad_digit_pattern
            elif bad_digit_pattern.is_eight():
                self.pattern_to_digit[bad_digit_pattern] = '8'
                self.digit_to_pattern['8'] = bad_digit_pattern

    def parse_bad_digit_values(self, bad_digit_values_str):
        for bad_digit_value in bad_digit_values_str.split(' '):
            self.bad_digit_values.append(BadDigit(bad_digit_value))

    def get_good_value(self):
        result = ''
        for bad_digit_value in self.bad_digit_values:
            result += bad_digit_value.to_good_string()
        return result

    def get_good_value_int(self):
        digits = []
        for bad_digit_value in self.bad_digit_values:
            digits.append(self.digit_from_pattern(bad_digit_value.value, Entry.CROSS_CONNECTION_MAPS[
                self.map_index]))
        value_str = ''.join(digits)
        if '.' in value_str:
            print('value_str={}'.format(value_str))
            print(self.to_string())
        return int(value_str)

    def to_string(self):
        result = ''
        result += 'entry:\n'
        result += '           bad_digit_patterns: '
        for bad_digit_pattern in self.bad_digit_patterns:
            result += '{0:>8}'.format(bad_digit_pattern.to_string())
            result += ', '
        result = result[:-2]
        result += '\n    translated_digit_patterns: '
        for bad_digit_pattern in self.bad_digit_patterns:
            result += '{0:>8}'.format(self.translate_pattern(bad_digit_pattern.to_string(),
                                                             Entry.CROSS_CONNECTION_MAPS[self.map_index]))
            result += ', '
        result = result[:-2]
        result += '\n            translated_digits: '
        for bad_digit_pattern in self.bad_digit_patterns:
            result += '{0:>8}'.format(self.digit_from_pattern(bad_digit_pattern.to_string(),
                                                              Entry.CROSS_CONNECTION_MAPS[self.map_index]))
            result += ', '
        result = result[:-2]
        result += '\n             bad_value_digits: '
        for bad_value_digit in self.bad_digit_values:
            result += '{0:>8}'.format(bad_value_digit.to_string())
            result += ', '
        result = result[:-2]
        result += '\n      translated_value_digits: '
        for bad_value_digit in self.bad_digit_values:
            result += '{0:>8}'.format(
                self.translate_pattern(bad_value_digit.to_string(), Entry.CROSS_CONNECTION_MAPS[self.map_index]))
            result += ', '
        result = result[:-2]
        result += '\n         cross_connection_map: {}'.format(Entry.CROSS_CONNECTION_MAPS[self.map_index])
        result += '\n                    map_index: {}\n'.format(self.map_index)
        return result


class Simulator(object):

    def __init__(self):
        self.entries = []

    def add_entry(self, input_line):
        self.entries.append(Entry(input_line))

    def run(self):
        self.count_easy_digits()

    def count_easy_digits(self):
        digit_counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for entry in self.entries:
            good_value = entry.get_good_value()
            if good_value:
                for digit in good_value:
                    if digit != '.':
                        digit_counts[int(digit)] += 1
        print('digit_counts: {}'.format(digit_counts))
        print('total 1, 4, 7, 8 digits: {}'.format(sum(digit_counts)))

    def sum_values(self):
        total = 0
        for entry in self.entries:
            total += entry.get_good_value_int()
        print('total={}', total)

    def to_string(self):
        result = ''
        for entry in self.entries:
            result += entry.to_string()
            result += '\n\n'
        return result


def main():
    simulator = Simulator()
    with open('../../data/day08.data', 'r') as data_file:
        input_line = data_file.readline().strip()
        while input_line:
            simulator.add_entry(input_line)
            input_line = data_file.readline().strip()
    simulator.count_easy_digits()
    simulator.sum_values()


main()
