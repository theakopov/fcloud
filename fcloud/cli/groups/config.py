from pathlib import Path
from os import environ
from typing import Optional

from ...utils.config import edit_config
from ...models.settings import UserArgument

from ...exceptions.driver_errors import DriverError
from ...exceptions.exceptions import FcloudException


class Config:
    """Use to edit the configuration"""

    def __init__(self, available_clouds: list[str], path: Optional[Path] = None):
        if path is None:
            path = Path(environ.get("FCLOUD_CONFIG_PATH"))  # type: ignore
        self._path = path
        self._available = available_clouds

    def set_cloud(self, name: UserArgument):
        """Setup your cloud"""
        if name in self._available:
            edit_config("FCLOUD", "service", str(name))
        else:
            title, message = DriverError.driver_error
            raise FcloudException(title, message.format(name))

    def set_main_folder(self, path: UserArgument):
        """Setup your main folder"""
        edit_config("FCLOUD", "main_folder", str(path))

    def set_cfl_ex(self, extension: UserArgument):
        """Setup your cfl_extension"""
        edit_config("FCLOUD", "cfl_extension", str(extension))

    def set_parametr(
        self, section: UserArgument, parametr_name: UserArgument, value: UserArgument
    ):
        "Set amy parametr to configuration"
        edit_config(str(section), str(parametr_name), str(value))

    cloud = set_cloud
    main_folder = folder = set_main_folder
    cfl_ex = extension = set_cfl_ex

    def path(self):
        """Config path"""
        return self._path

    def read(self) -> str:
        """Text of the config file"""
        with open(self._path, "r") as config:
            return config.read()
