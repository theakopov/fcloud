from enum import Enum
from dataclasses import dataclass
from pathlib import Path

from ..drivers.dropbox.models import DropboxAuth


class AuthData(Enum):
    dropbox = DropboxAuth


@dataclass(frozen=True)
class Config:
    service: str
    main_folder: Path
    auth: AuthData
    cfl_extension: str
