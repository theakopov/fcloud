from dataclasses import dataclass
from typing import TypeVar

from ..drivers.base import CloudProtocol

T = TypeVar("T")  # Fields requested by the driver from the config


@dataclass
class Driver:
    name: str
    driver: CloudProtocol
    auth_model: T
