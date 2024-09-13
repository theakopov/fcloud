from typing import TypeVar
from typing import Generic
from typing import Type
from dataclasses import dataclass

from ..drivers.base import CloudProtocol

T = TypeVar("T")  # Dataclasses with fields requested by the driver from the config


@dataclass
class Driver:
    name: str
    driver: Type[CloudProtocol]
    auth_model: Type[T]
