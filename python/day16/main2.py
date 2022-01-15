import time

from bitarray import bitarray
from enum import Enum
import sys
from abc import abstractmethod, ABC

from typing import Tuple


class Packet(ABC):
    class Type(Enum):
        SUM = 0
        PRODUCT = 1
        MIN = 2
        MAX = 3
        LITERAL = 4
        GREATER_THAN = 5
        LESS_THAN = 6
        EQUAL_TO = 7

    VERSION_OFFSET = 0
    VERSION_LENGTH = 3
    TYPE_OFFSET = 3
    TYPE_LENGTH = 3
    HEADER_LENGTH = TYPE_OFFSET + TYPE_LENGTH

    def __init__(self, packet_bits: bitarray) -> None:
        ABC.__init__(self)
        self.packet_bits = packet_bits

    def version(self) -> int:
        return Packet._version(self.packet_bits)

    @staticmethod
    def _version(packet_bits: bitarray) -> int:
        return int(packet_bits[Packet.VERSION_OFFSET:Packet.VERSION_OFFSET + Packet.VERSION_LENGTH].to01(), 2)

    def p_type(self) -> int:
        return Packet._p_type(self.packet_bits)

    @staticmethod
    def _p_type(packet_bits: bitarray) -> int:
        return int(packet_bits[Packet.TYPE_OFFSET:Packet.TYPE_OFFSET + Packet.TYPE_LENGTH].to01(), 2)

    def is_operator(self) -> bool:
        return not self.is_literal()

    def is_sum(self) -> bool:
        return Packet._is_sum(self.packet_bits)

    @staticmethod
    def _is_sum(packet_bits: bitarray) -> bool:
        return bool(Packet._p_type(packet_bits) == Packet.Type.SUM.value)

    def is_product(self) -> bool:
        return Packet._is_product(self.packet_bits)

    @staticmethod
    def _is_product(packet_bits: bitarray) -> bool:
        return bool(Packet._p_type(packet_bits) == Packet.Type.PRODUCT.value)

    def is_min(self) -> bool:
        return Packet._is_min(self.packet_bits)

    @staticmethod
    def _is_min(packet_bits: bitarray) -> bool:
        return bool(Packet._p_type(packet_bits) == Packet.Type.MIN.value)

    def is_max(self) -> bool:
        return Packet._is_max(self.packet_bits)

    @staticmethod
    def _is_max(packet_bits: bitarray) -> bool:
        return bool(Packet._p_type(packet_bits) == Packet.Type.MAX.value)

    def is_literal(self) -> bool:
        return Packet._is_literal(self.packet_bits)

    @staticmethod
    def _is_literal(packet_bits: bitarray) -> bool:
        return bool(Packet._p_type(packet_bits) == Packet.Type.LITERAL.value)

    def is_greater_than(self) -> bool:
        return Packet._is_greater_than(self.packet_bits)

    @staticmethod
    def _is_greater_than(packet_bits: bitarray) -> bool:
        return bool(Packet._p_type(packet_bits) == Packet.Type.GREATER_THAN.value)

    def is_less_than(self) -> bool:
        return Packet._is_less_than(self.packet_bits)

    @staticmethod
    def _is_less_than(packet_bits: bitarray) -> bool:
        return bool(Packet._p_type(packet_bits) == Packet.Type.LESS_THAN.value)

    def is_equal_to(self) -> bool:
        return Packet._is_equal_to(self.packet_bits)

    @staticmethod
    def _is_equal_to(packet_bits: bitarray) -> bool:
        return bool(Packet._p_type(packet_bits) == Packet.Type.EQUAL_TO.value)

    @staticmethod
    def make_packet(packet_bits: bitarray) -> 'Packet':
        if Packet._is_sum(packet_bits):
            new_packet = SumPacket(packet_bits)
        elif Packet._is_product(packet_bits):
            new_packet = ProductPacket(packet_bits)
        elif Packet._is_min(packet_bits):
            new_packet = MinPacket(packet_bits)
        elif Packet._is_max(packet_bits):
            new_packet = MaxPacket(packet_bits)
        elif Packet._is_literal(packet_bits):
            new_packet = LiteralPacket(packet_bits)
        elif Packet._is_greater_than(packet_bits):
            new_packet = GreaterThanPacket(packet_bits)
        elif Packet._is_less_than(packet_bits):
            new_packet = LessThanPacket(packet_bits)
        elif Packet._is_equal_to(packet_bits):
            new_packet = EqualToPacket(packet_bits)
        else:
            sys.exit(f'Unsupported packet type: {Packet._p_type(packet_bits)}')

        return new_packet

    @abstractmethod
    def value(self) -> Tuple[int, int, int]:
        return


class LiteralPacket(Packet):
    VALUE_GROUP_OFFSET = Packet.TYPE_OFFSET + Packet.TYPE_LENGTH
    VALUE_GROUP_LENGTH = 5

    def __init__(self, packet_bits: bitarray) -> None:
        Packet.__init__(self, packet_bits)

    def value(self) -> Tuple[int, int, int]:
        value = i = 0
        bit_count = Packet.HEADER_LENGTH
        done = False
        while not done:
            value_group = self.get_value_group(i)
            value = (value << (LiteralPacket.VALUE_GROUP_LENGTH - 1)) | int(value_group[1:].to01(), 2)
            bit_count += LiteralPacket.VALUE_GROUP_LENGTH
            done = value_group[0] == 0
            i += 1
        return self.version(), bit_count, value

    def get_value_group(self, group_index: int) -> bitarray:
        start_index = LiteralPacket.VALUE_GROUP_OFFSET + (LiteralPacket.VALUE_GROUP_LENGTH * group_index)
        return self.packet_bits[start_index:start_index + LiteralPacket.VALUE_GROUP_LENGTH]

    def length_bits(self) -> int:
        packet_length_bits = LiteralPacket.VALUE_GROUP_OFFSET
        done = False
        i = 0
        while not done:
            value_group = self.get_value_group(i)
            done = value_group[0] == 0
            packet_length_bits += LiteralPacket.VALUE_GROUP_LENGTH
            i += 1
        return packet_length_bits


class OperatorPacket(Packet):
    MODE_OFFSET = Packet.TYPE_OFFSET + Packet.TYPE_LENGTH
    MODE_LENGTH = 1
    LENGTH_BITS_OFFSET = MODE_OFFSET + MODE_LENGTH
    LENGTH_BITS_LENGTH = 15
    LENGTH_PACKETS_OFFSET = LENGTH_BITS_OFFSET
    LENGTH_PACKETS_LENGTH = 11
    SUB_PACKETS_BIT_MODE_OFFSET = LENGTH_BITS_OFFSET + LENGTH_BITS_LENGTH
    SUB_PACKETS_PACKET_MODE_OFFSET = LENGTH_PACKETS_OFFSET + LENGTH_PACKETS_LENGTH

    def __init__(self, packet_bits: bitarray) -> None:
        Packet.__init__(self, packet_bits)

    def is_bit_mode(self) -> bool:
        start_index = OperatorPacket.MODE_OFFSET
        return bool(self.packet_bits[start_index] == 0)

    def is_packet_mode(self) -> bool:
        return not self.is_bit_mode()

    def sub_packets_bit_length(self) -> int:
        start_index = OperatorPacket.LENGTH_BITS_OFFSET
        end_index = start_index + OperatorPacket.LENGTH_BITS_LENGTH
        return int(self.packet_bits[start_index:end_index].to01(), 2)

    def sub_packets_packet_length(self) -> int:
        start_index = OperatorPacket.LENGTH_PACKETS_OFFSET
        end_index = start_index + OperatorPacket.LENGTH_PACKETS_LENGTH
        return int(self.packet_bits[start_index:end_index].to01(), 2)

    def sub_packet_bits(self) -> int:
        if self.is_bit_mode():
            return self.packet_bits[OperatorPacket.SUB_PACKETS_BIT_MODE_OFFSET:]
        else:
            return self.packet_bits[OperatorPacket.SUB_PACKETS_PACKET_MODE_OFFSET:]

    def length_bits(self) -> int:
        if self.is_bit_mode():
            packet_length_bits = OperatorPacket.SUB_PACKETS_BIT_MODE_OFFSET
            packet_length_bits += OperatorPacket.LENGTH_BITS_LENGTH
        else:
            packet_length_bits = OperatorPacket.SUB_PACKETS_PACKET_MODE_OFFSET
            packet_length_bits += OperatorPacket.LENGTH_PACKETS_LENGTH
        packet_length_bits += self.sub_packets_bit_length()
        return packet_length_bits

    def apply(self, operation: 'function') -> Tuple[int, int, int]:
        version_sum = 0
        bit_count = 0
        packet_count = 0
        values = []
        done = False
        while not done:
            sub_packet = Packet.make_packet(self.sub_packet_bits()[bit_count:])
            sub_version_sum, bits_processed, sub_value = sub_packet.value()
            values.append(sub_value)
            bit_count += bits_processed
            version_sum += sub_version_sum
            packet_count += 1
            if self.is_bit_mode():
                if bit_count >= self.sub_packets_bit_length():
                    done = True
            else:
                if packet_count >= self.sub_packets_packet_length():
                    done = True
        version_sum += self.version()
        if self.is_bit_mode():
            bit_count += OperatorPacket.SUB_PACKETS_BIT_MODE_OFFSET
        else:
            bit_count += OperatorPacket.SUB_PACKETS_PACKET_MODE_OFFSET

        return version_sum, bit_count, operation(values)

    @abstractmethod
    def value(self) -> Tuple[int, int, int]:
        return


class SumPacket(OperatorPacket):

    def __init__(self, packet_bits: bitarray) -> None:
        OperatorPacket.__init__(self, packet_bits)

    @staticmethod
    def operation(values: list) -> int:
        return sum(values)

    def value(self) -> Tuple[int, int, int]:
        return self.apply(self.operation)


class ProductPacket(OperatorPacket):

    def __init__(self, packet_bits: bitarray) -> None:
        OperatorPacket.__init__(self, packet_bits)

    @staticmethod
    def operation(values: list) -> int:
        result = 1
        for value in values:
            result *= value
        return result

    def value(self) -> Tuple[int, int, int]:
        return self.apply(self.operation)


class MinPacket(OperatorPacket):

    def __init__(self, packet_bits: bitarray) -> None:
        OperatorPacket.__init__(self, packet_bits)

    @staticmethod
    def operation(values: list) -> int:
        return min(values)

    def value(self) -> int:
        return self.apply(self.operation)


class MaxPacket(OperatorPacket):

    def __init__(self, packet_bits) -> None:
        OperatorPacket.__init__(self, packet_bits)

    @staticmethod
    def operation(values: list) -> int:
        return max(values)

    def value(self) -> int:
        return self.apply(self.operation)


class GreaterThanPacket(OperatorPacket):

    def __init__(self, packet_bits: bitarray) -> None:
        OperatorPacket.__init__(self, packet_bits)

    @staticmethod
    def operation(values: list) -> int:
        return int(values[0] > values[1])

    def value(self) -> int:
        return self.apply(self.operation)


class LessThanPacket(OperatorPacket):

    def __init__(self, packet_bits: bitarray) -> None:
        OperatorPacket.__init__(self, packet_bits)

    @staticmethod
    def operation(values) -> int:
        return int(values[0] < values[1])

    def value(self) -> Tuple[int, int, int]:
        return self.apply(self.operation)


class EqualToPacket(OperatorPacket):

    def __init__(self, packet_bits: bitarray) -> None:
        OperatorPacket.__init__(self, packet_bits)

    @staticmethod
    def operation(values: list) -> int:
        return int(values[0] == values[1])

    def value(self) -> int:
        return self.apply(self.operation)


def elapsed_time(start_time: int, end_time: int) -> str:
    t = end_time - start_time
    unit = 'seconds'
    if t < 1:
        t = t * 1000
        unit = 'milliseconds'
    if t < 1:
        t = t * 1000
        unit = 'microseconds'
    if t < 1:
        t = t * 1000
        unit = 'nanoseconds'

    return f'{t:.2f} {unit}'


def init_data() -> bitarray:
    with open('data.txt', 'r') as data_file:
        line = data_file.readline()
    packet_bits = bitarray()
    for i in range(0, len(line), 2):
        packet_bits.extend(format(int(line[i:i + 2], 16), '08b'))
    return packet_bits


def main() -> None:
    packet_bits = init_data()

    start_time = time.perf_counter()
    version_sum, bit_count, value = Packet.make_packet(packet_bits).value()
    end_time = time.perf_counter()
    print(f'Part 1, version_sum = {version_sum}')
    print(f'Part 2, value = {value}')
    print(f'Elapsed time: {elapsed_time(start_time, end_time)}')


if __name__ == '__main__':
    main()
