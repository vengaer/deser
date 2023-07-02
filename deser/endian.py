import enum

class Endianness(enum.Enum):
    LITTLE = '<'
    BIG = '>'
    NATIVE = '@'
    NETWORK = '!'
    NATIVE_PACKED = '='
