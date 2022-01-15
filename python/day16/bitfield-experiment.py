import ctypes

c_ubyte = ctypes.c_ubyte
c_uint32 = ctypes.c_uint32

DATA = 0b110100101111111000101000


# class AbstractPacket(ctypes.LittleEndianStructure):
#     _fields_ = [
#         ("version", c_uint32, 3),
#         ("type", c_uint32, 3)
#     ]
#     #
#     # def __init__(self):
#     #     super(AbstractPacket, self).__init__()
#     #     self.data = data

# version 2, length 16
# version 6, length 11

class LiteralPacketV2(ctypes.BigEndianStructure):
    _fields_ = [
        ("filler", c_uint32, 8),
        ("version", c_uint32, 3),
        ("type", c_uint32, 3),
        ("check_bit_1", c_uint32, 1),
        ("nibble_1", c_uint32, 4),
        ("check_bit_2", c_uint32, 1),
        ("nibble_2", c_uint32, 4),
        ("check_bit_3", c_uint32, 1),
        ("nibble_3", c_uint32, 4),
    ]

    def value(self):
        return self.nibble_1 << 8 | self.nibble_2 << 4 | self.nibble_3


class LiteralPacketV6(ctypes.BigEndianStructure):
    _fields_ = [
        ("filler", c_uint32, 8),
        ("version", c_uint32, 3),
        ("type", c_uint32, 3),
        ("check_bit_1", c_uint32, 1),
        ("nibble_1", c_uint32, 4),
        ("check_bit_2", c_uint32, 1),
        ("nibble_2", c_uint32, 4),
        ("check_bit_3", c_uint32, 1),
        ("nibble_3", c_uint32, 4),
    ]

    def value(self):
        return self.nibble_1 << 8 | self.nibble_2 << 4 | self.nibble_3


class OperatorPacket(ctypes.BigEndianStructure):
    _fields_ = [
        ("version", c_uint32, 3),
        ("type", c_uint32, 3),
        ("mode", c_uint32, 1)
    ]


class BitModeOperatorPacket(ctypes.BigEndianStructure):
    _fields_ = [
        ("version", c_uint32, 3),
        ("type", c_uint32, 3),
        ("mode", c_uint32, 1),
        ("length_bits", c_uint32, 15),
        ("sub_packet_1", c_uint32, 11),
        ("sub_packet_2", c_uint32, 16)
    ]


class PacketModeOperatorPacket(ctypes.BigEndianStructure):
    _fields_ = [
        ("version", c_uint32, 3),
        ("type", c_uint32, 3),
        ("mode", c_uint32, 1),
        ("length_packets", c_uint32, 11),
        ("sub_packet_1", c_uint32, 11),
        ("sub_packet_2", c_uint32, 16)
    ]

    def value(self):
        return self.nibble_1 << 8 | self.nibble_2 << 4 | self.nibble_3


# class MyBits(ctypes.Structure):
#     _fields_ = [
#         ("bitfield_1", c_uint32, 1),
#         ("bitfield_2", c_uint32, 1),
#         ("bitfield_3", c_uint32, 1),
#         ("bitfield_4", c_uint32, 1),
#         ("bitfield_5", c_uint32, 1),
#         ("bitfield_6", c_uint32, 1),
#         ("bitfield_7", c_uint32, 1),
#         ("bitfield_8", c_uint32, 1),
#         ("bitfield_9", c_uint32, 1),
#         ("bitfield_10", c_uint32, 1),
#         ("bitfield_11", c_uint32, 1),
#         ("bitfield_12", c_uint32, 1),
#         ("bitfield_13", c_uint32, 1),
#         ("bitfield_14", c_uint32, 1),
#         ("bitfield_15", c_uint32, 1),
#         ("bitfield_16", c_uint32, 1),
#     ]


class MyBits(ctypes.BigEndianStructure):
    _fields_ = [
        ("bitfield_1", c_ubyte, 1),
        ("bitfield_2", c_ubyte, 1),
        ("bitfield_3", c_ubyte, 1),
        ("bitfield_4", c_ubyte, 1),
        ("bitfield_5", c_ubyte, 1),
        ("bitfield_6", c_ubyte, 1),
        ("bitfield_7", c_ubyte, 1),
        ("bitfield_8", c_ubyte, 1),
        ("bitfield_9", c_ubyte, 1),
        ("bitfield_10", c_ubyte, 1),
        ("bitfield_11", c_ubyte, 1),
        ("bitfield_12", c_ubyte, 1),
        ("bitfield_13", c_ubyte, 1),
        ("bitfield_14", c_ubyte, 1),
        ("bitfield_15", c_ubyte, 1),
        ("bitfield_16", c_ubyte, 1),
        ("bitfield_17", c_ubyte, 1),
        ("bitfield_18", c_ubyte, 1),
        ("bitfield_19", c_ubyte, 1),
        ("bitfield_20", c_ubyte, 1),
        ("bitfield_21", c_ubyte, 1),
        ("bitfield_22", c_ubyte, 1),
        ("bitfield_23", c_ubyte, 1),
        ("bitfield_24", c_ubyte, 1),
        ("bitfield_25", c_ubyte, 1),
        ("bitfield_26", c_ubyte, 1),
        ("bitfield_27", c_ubyte, 1),
        ("bitfield_28", c_ubyte, 1),
        ("bitfield_29", c_ubyte, 1),
        ("bitfield_30", c_ubyte, 1),
        ("bitfield_31", c_ubyte, 1),
        ("bitfield_32", c_ubyte, 1),
    ]


class Packet(ctypes.Union):
    _anonymous_ = ("bit", "bit2")
    _fields_ = [
        ("bit2", MyBits),
        ("bit", LiteralPacket),
        ("asByte", ctypes.c_ubyte * 4)
    ]


packet = Packet()
buffer = bytearray([0b00000000, 0b11010010, 0b11111110, 0b00101000])
mytype = ctypes.c_ubyte * 4
packet.asByte = mytype.from_buffer(buffer)
print(f'DATA={DATA}')

print(f'version={packet.version:03b}')
print(f'type={packet.type:03b}')
print(f'check_bit_1={packet.check_bit_1:01b}')
print(f'nibble_1={packet.nibble_1:04b}')
print(f'check_bit_2={packet.check_bit_2:01b}')
print(f'nibble_2={packet.nibble_2:04b}')
print(f'check_bit_3={packet.check_bit_3:01b}')
print(f'nibble_3={packet.nibble_3:04b}')

# if isinstance(packet, LiteralPacket):
print(f'value={packet.bit.value()}')

# if not isinstance(packet, MyBits):
#     exit(0)

print('00000000 11010010 11111110 00101000')
print(f'{packet.bit2.bitfield_1}', end='')
print(f'{packet.bitfield_2}', end='')
print(f'{packet.bitfield_3}', end='')
print(f'{packet.bitfield_4}', end='')
print(f'{packet.bitfield_5}', end='')
print(f'{packet.bitfield_6}', end='')
print(f'{packet.bitfield_7}', end='')
print(f'{packet.bitfield_8}', end='')

print(f' {packet.bitfield_9}', end='')
print(f'{packet.bitfield_10}', end='')
print(f'{packet.bitfield_11}', end='')
print(f'{packet.bitfield_12}', end='')
print(f'{packet.bitfield_13}', end='')
print(f'{packet.bitfield_14}', end='')
print(f'{packet.bitfield_15}', end='')
print(f'{packet.bitfield_16}', end='')

print(f' {packet.bitfield_17}', end='')
print(f'{packet.bitfield_18}', end='')
print(f'{packet.bitfield_19}', end='')
print(f'{packet.bitfield_20}', end='')
print(f'{packet.bitfield_21}', end='')
print(f'{packet.bitfield_22}', end='')
print(f'{packet.bitfield_23}', end='')
print(f'{packet.bitfield_24}', end='')

print(f' {packet.bitfield_25}', end='')
print(f'{packet.bitfield_26}', end='')
print(f'{packet.bitfield_27}', end='')
print(f'{packet.bitfield_28}', end='')
print(f'{packet.bitfield_29}', end='')
print(f'{packet.bitfield_30}', end='')
print(f'{packet.bitfield_31}', end='')
print(f'{packet.bitfield_32}')

# print(f' bitfield_1={packet.bitfield_1}')
# print(f' bitfield_2={packet.bitfield_2}')
# print(f' bitfield_3={packet.bitfield_3}')
# print(f' bitfield_4={packet.bitfield_4}')
# print(f' bitfield_5={packet.bitfield_5}')
# print(f' bitfield_6={packet.bitfield_6}')
# print(f' bitfield_7={packet.bitfield_7}')
# print(f' bitfield_8={packet.bitfield_8}')
#
# print(f' bitfield_9={packet.bitfield_9}')
# print(f'bitfield_10={packet.bitfield_10}')
# print(f'bitfield_11={packet.bitfield_11}')
# print(f'bitfield_12={packet.bitfield_12}')
# print(f'bitfield_13={packet.bitfield_13}')
# print(f'bitfield_14={packet.bitfield_14}')
# print(f'bitfield_15={packet.bitfield_15}')
# print(f'bitfield_16={packet.bitfield_16}')
#
# print(f'bitfield_17={packet.bitfield_17}')
# print(f'bitfield_18={packet.bitfield_18}')
# print(f'bitfield_19={packet.bitfield_19}')
# print(f'bitfield_20={packet.bitfield_20}')
# print(f'bitfield_21={packet.bitfield_21}')
# print(f'bitfield_22={packet.bitfield_22}')
# print(f'bitfield_23={packet.bitfield_23}')
# print(f'bitfield_24={packet.bitfield_24}')
#
# print(f'bitfield_25={packet.bitfield_25}')
# print(f'bitfield_26={packet.bitfield_26}')
# print(f'bitfield_27={packet.bitfield_27}')
# print(f'bitfield_28={packet.bitfield_28}')
# print(f'bitfield_29={packet.bitfield_29}')
# print(f'bitfield_30={packet.bitfield_30}')
# print(f'bitfield_31={packet.bitfield_31}')
# print(f'bitfield_32={packet.bitfield_32}')


# print(
#     'version={}, type={}, check_bit_1={}, nibble_1={}, check_bit_2={}, nibble_2={}, check_bit_3={}, nibble_3={}'.format(
#         bin(packet.version), bin(packet.type), bin(packet.check_bit_1), bin(packet.nibble_1),
#         bin(packet.check_bit_2), bin(packet.nibble_2), bin(packet.check_bit_3), bin(packet.nibble_3)))
# print('version={}, type={}, check_bit_1={}, nibble_1={}, check_bit_2={}, nibble_2={}, check_bit_3={}, '
#       'nibble_3={}'.format(packet.version, packet.type, packet.check_bit_1, packet.nibble_1, packet.check_bit_2,
#                            packet.nibble_2, packet.check_bit_3,
#                            packet.nibble_3))
