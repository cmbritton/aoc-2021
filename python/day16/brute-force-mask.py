import timeit

import numpy as np

PACKET_TYPE_LITERAL = 4
PACKET_LITERAL_LENGTH_BYTES = 3
PACKET_VERSION_MASK = 0b11100000
PACKET_VERSION_SHIFT = 5
PACKET_TYPE_MASK = 0b00011100
PACKET_TYPE_SHIFT = 2

LITERAL_CHECK_BIT_1_MASK = 0b00000010
LITERAL_CHECK_BIT_2_MASK = 0b00010000
LITERAL_CHECK_BIT_3_MASK = 0b10000000
LITERAL_EXPECTED_CHECK_BITS = LITERAL_CHECK_BIT_1_MASK | LITERAL_CHECK_BIT_2_MASK | LITERAL_CHECK_BIT_3_MASK
LITERAL_VALUE_BYTE_1_MASK = 0b00000001
LITERAL_VALUE_BYTE_2_MASK = 0b00001111
LITERAL_VALUE_BYTE_3_MASK = 0b01111000

OPERATOR_LENGTH_TYPE_MASK = 0b00000010
OPERATOR_BYTE_1_LENGTH_BITS_MASK = 0b00000001
OPERATOR_BYTE_2_LENGTH_BITS_MASK = 0b11111111
OPERATOR_BYTE_3_LENGTH_BITS_MASK = 0b11111100

packet_data = None

version_sum = 0


def literal_check_bits(packet_start_index):
    check_bit_1 = packet_data[packet_start_index] & LITERAL_CHECK_BIT_1_MASK
    check_bit_2 = packet_data[packet_start_index + 1] & LITERAL_CHECK_BIT_2_MASK
    check_bit_3 = packet_data[packet_start_index + 2] & LITERAL_CHECK_BIT_3_MASK
    return check_bit_1 | check_bit_2 | check_bit_3


def literal_check_bits_valid(packet_start_index):
    return literal_check_bits(packet_start_index) == LITERAL_EXPECTED_CHECK_BITS


def literal_value(packet_start_index):
    if not literal_check_bits_valid(packet_start_index):
        print('ERROR: Invalid literal packet check bits for packet at offset {}'.format(packet_start_index))
    value = (packet_data[packet_start_index] & LITERAL_BYTE_1_MASK) << 8
    value |= packet_data[packet_start_index + 1] & LITERAL_BYTE_2_MASK << 4
    return value | packet_data[packet_start_index + 2] & LITERAL_BYTE_3_MASK


def literal_packet(packet_start_index):
    return packet_type(packet_start_index) == 4


def packet_version(packet_start_index):
    return int(packet_data[packet_start_index] & PACKET_VERSION_MASK) >> PACKET_VERSION_SHIFT


def packet_type(packet_start_index):
    return int(packet_data[packet_start_index] & PACKET_TYPE_MASK) >> PACKET_TYPE_SHIFT


def bit_length_mode(packet_start_index):
    return not packet_length_mode_packet_length(packet_start_index)


def packet_length_mode_packet_length(packet_start_index):
    return packet_data[packet_start_index] & OPERATOR_LENGTH_TYPE_MASK


def sub_packet_length_bits(packet_start_index):
    value = (packet_data[packet_start_index] & OPERATOR_BYTE_1_LENGTH_BITS_MASK) << 14
    value |= packet_data[packet_start_index + 1] << 6
    return value | (packet_data[packet_start_index + 2] & OPERATOR_BYTE_3_LENGTH_BITS_MASK)


def operator_packet_length_bytes(packet_start_index):
    if bit_length_mode(packet_start_index):
        return sub_packet_length_bits(packet_start_index)
    else:
        return packet_length_mode_packet_length(packet_start_index)


def packet_length_bytes(packet_start_index):
    if literal_packet(packet_start_index):
        return 3
    else:
        return operator_packet_length_bytes(packet_start_index)


def process_packet(packet_start_index):
    global version_sum
    process_packet(packet_start_index + get_packet_length_bytes())
    version_sum += get_packet_version(packet_start_index)


def setup_globals():
    global version_sum
    version_sum = 0


def print_results(part, elapsed_time_seconds):
    global version_sum
    print('\nPart {}'.format(part))
    print('version sum: {}'.format(version_sum))
    print('Elapsed time: {} seconds'.format(elapsed_time_seconds))
    # print('Path length:         {} hops'.format(len(path_to_list())))
    # print('Path:                {}'.format(path_to_string()))


def init_data():
    with open('../../data/day16.data', 'r') as data_file:
        line = data_file.readline()

    global packet_data
    packet_data = np.zeros((len(line) * 4,), dtype=np.ubyte)
    hex_bytes = [line[i:i + 2] for i in range(0, len(line), 2)]
    for i in range(len(hex_bytes)):
        data_byte = int(hex_bytes[i], 16)
        packet_data[i] = data_byte & 0xff
    print()


def do_run(part):
    global packet_data
    setup_globals()
    t = timeit.Timer(lambda: process_packet(0))
    elapsed_time_seconds = t.timeit(1)
    print_results(part, elapsed_time_seconds)


def main():
    global packet_data
    init_data()
    do_run(1)

    # risk_levels = expand_risk_levels()
    # do_run(2)


if __name__ == '__main__':
    main()
