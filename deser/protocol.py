import io
import typing

from typing import Any, Protocol, Union

from .endian import Endianness

@typing.runtime_checkable
class Serializable(Protocol):
    def __init__(self, value: Any) -> None:
        ...

    def serialize(self, endianness: Endianness = Endianness.NETWORK) -> bytes:
        ...

    def deserialize(self, data: Union[bytes, io.BytesIO], endianness: Endianness = Endianness.NETWORK) -> 'Serializable':
        ...
