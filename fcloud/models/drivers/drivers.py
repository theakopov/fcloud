from enum import Enum

from ...drivers.dropbox_driver import DropboxCloud


class Drivers(Enum):
    dropbox = DropboxCloud
