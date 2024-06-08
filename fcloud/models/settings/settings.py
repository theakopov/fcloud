from enum import Enum
from dataclasses import dataclass
from pathlib import Path

from .driver_settings_models import DropboxAuth
from ..clouds import CloudEnum


class AuthData(Enum):
    dropbox = DropboxAuth


@dataclass(frozen=True)
class Config:
    service: CloudEnum
    main_folder: Path
    auth: AuthData
    cfl_extension: str
