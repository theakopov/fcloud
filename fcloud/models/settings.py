from dataclasses import dataclass
from pathlib import Path

from .driver import Driver


@dataclass(frozen=True)
class Config:
    service: Driver
    main_folder: Path
    cfl_extension: str
