import dataclasses
import io
import typing

from typing import Generator, List, Tuple, Type, TypeVar, Union

from .endian import Endianness
from .protocol import Serializable

_T = TypeVar('_T')

def serializable(cls: Type[_T]) -> Type[_T]:
    dataclasses.dataclass(cls)

    def _all_fields(cls) -> Generator[Tuple[str, Serializable], None, None]:
        for hint in typing.get_type_hints(cls).items():
            yield hint

    def _serialize(self, endianness: Endianness = Endianness.NETWORK) -> bytes:
        data = bytearray()
        for field, hint in self._all_fields():
            val = getattr(self, field)
            if not isinstance(val, Serializable):
                val = hint(val)
            data += val.serialize()
        return data

    def _deserialize(data: Union[bytes, io.BytesIO], endianness: Endianness = Endianness.NETWORK) -> _T:
        if not isinstance(data, io.BytesIO):
            data = io.BytesIO(data)

        unpacked: List[Serializable] = []
        for field, hint in _all_fields(cls):
            unpacked += [hint.deserialize(data, endianness)]

        return cls(*unpacked)

    setattr(cls, '_all_fields', _all_fields)
    setattr(cls, 'serialize', _serialize)
    setattr(cls, 'deserialize', _deserialize)

    return cls
