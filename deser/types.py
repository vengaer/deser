import abc
import io
import struct
import typing

from typing import Generic, Literal, Sequence, Union, Type, TypeVar

from .exception import InvalidArrayInitializer
from .endian import Endianness
from .protocol import Serializable

class Integer:
    def __init__(self, value: Union[bool, int]) -> None:
        self._value = value

    @property
    def value(self) -> Union[bool, int]:
        return self._value

    @classmethod
    @abc.abstractmethod
    def formatchar(cls) -> str:
        ...

    def serialize(self, endianness: Endianness = Endianness.NETWORK) -> bytes:
        return struct.pack(endianness.value + self.formatchar(), self.value)

    @classmethod
    def deserialize(cls, data: Union[bytes, io.BytesIO], endianness: Endianness = Endianness.NETWORK) -> 'Integer':
        if not isinstance(data, io.BytesIO):
            data = io.BytesIO(data)
        full_format = endianness.value + cls.formatchar()
        return struct.unpack(full_format, data.read(struct.calcsize(full_format)))[0]

class _Bool(Integer):
    @classmethod
    def formatchar(self) -> str:
        return '?'

class I8(Integer):
    @classmethod
    def formatchar(cls) -> str:
        return 'b'

class U8(Integer):
    @classmethod
    def formatchar(cls) -> str:
        return 'B'

class I16(Integer):
    @classmethod
    def formatchar(cls) -> str:
        return 'h'

class U16(Integer):
    @classmethod
    def formatchar(clar) -> str:
        return 'H'

class I32(Integer):
    @classmethod
    def formatchar(cls) -> str:
        return 'l'

class U32(Integer):
    @classmethod
    def formatchar(cls) -> str:
        return 'L'

class I64(Integer):
    @classmethod
    def formatchar(cls) -> str:
        return 'q'

class U64(Integer):
    @classmethod
    def formatchar(cls) -> str:
        return 'Q'

class SSizeT(Integer):
    @classmethod
    def formatchar(cls) -> str:
        return 'n'

class SizeT(Integer):
    @classmethod
    def formatchar(cls) -> str:
        return 'N'

_T = TypeVar('_T', bound=Serializable)
_Size = TypeVar('_Size')

class Array(Generic[_T, _Size]):
    def __init__(self, values: Sequence[_T]) -> None:
        self._values = values

    @property
    def underlying_type(self) -> Type[_T]:
        return self.__orig_class__.__args__[0]

    def __len__(self) -> int:
        return typing.get_args(self.__orig_class__.__args__[1])[0]

    @property
    def values(self) -> Sequence[_T]:
        return self._values

    def serialize(self, endianness: Endianness = Endianness.NETWORK) -> bytes:
        if len(self._values) != len(self):
            raise InvalidArrayInitializer(len(self), len(self.values))

        return b''.join([self.underlying_type(d).serialize(endianness) for d in self.values])

    @classmethod
    def deserialize(cls, data: Union[bytes, io.BytesIO], endianness: Endianness = Endianness.NETWORK) -> 'Array':
        # todo
        ...

Literal = typing.Literal
