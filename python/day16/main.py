import timeit

# This one stumped me. Went down several wrong avenues like ctypes and asn1 before conceding defeat and
# using https://github.com/benediktwerner/AdventOfCode/blob/master/2021/day16/sol.py
# as a guide. So, I cannot really claim to have solved this one.

PACKET_TYPE_LITERAL = 4
LENGTH_MODE_BITS = 0
LENGTH_MODE_PACKETS = 1


def process_packet(packet):
    p_version = int(packet[:3], 2)
    p_type = int(packet[3:6], 2)
    value = sub_version = 0
    if p_type == PACKET_TYPE_LITERAL:
        value_bits = packet[6:]
        while True:
            value <<= 4
            value |= int(value_bits[1:5], 2)
            if value_bits[0] == '0':
                return p_version, value, value_bits[5:]
            value_bits = value_bits[5:]
    else:
        length_mode = int(packet[6:7], 2)
        if length_mode == LENGTH_MODE_BITS:
            length_bits = int(packet[7:22], 2)
            my_bits, sub_packet = packet[22:22 + length_bits], packet[22 + length_bits:]
            while my_bits:
                sub_version, value, my_bits = process_packet(my_bits)
                p_version += sub_version
        else:
            length_mode_packets = int(packet[7:18], 2)
            sub_packet = packet[18:]
            for _ in range(length_mode_packets):
                sub_version, value, sub_packet = process_packet(sub_packet)
                p_version += sub_version

    return p_version, value, sub_packet


def setup_globals():
    version_sum = 0


def print_results(part, version_sum):
    print('\nPart {}'.format(part))
    print('version sum: {}'.format(version_sum))
    # print('Elapsed time: {} seconds'.format(elapsed_time_seconds))
    # print('Path length:         {} hops'.format(len(path_to_list())))
    # print('Path:                {}'.format(path_to_string()))


def init_data():
    with open('data.txt', 'r') as data_file:
        line = data_file.readline()
    return ''.join(f'{int(b, 16):04b}' for b in line)


def do_run(part, packet):
    setup_globals()
    version_sum, value, sub_packet = process_packet(packet)
    # t = timeit.Timer(lambda: process_packet(packet))
    # elapsed_time_seconds = t.timeit(1)
    print_results(part, version_sum)


def main():
    packet = init_data()
    do_run(1, packet)

    # risk_levels = expand_risk_levels()
    # do_run(2)


if __name__ == '__main__':
    main()
