from enum import Enum

from ..drivers.dropbox.dropbox import DropboxCloud


class Drivers(Enum):
    dropbox = DropboxCloud
