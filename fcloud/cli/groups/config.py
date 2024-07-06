from pathlib import Path
from os import environ
from typing import Optional

from ...utils.config import edit_config

from ...exceptions.driver_errors import DriverError
from ...exceptions.exceptions import FcloudException


class Config:
    """Use to edit the configuration"""

    def __init__(self, available_clouds: list[str], path: Optional[Path] = None):
        if path is None:
            path = Path(environ.get("FCLOUD_CONFIG_PATH"))
        self._path = path
        self._available = available_clouds

    def set_cloud(self, name: str):
        """Setup your cloud"""
        if name in self._available:
            edit_config("FCLOUD", "service", name)
        else:
            title, message = DriverError.driver_error
            raise FcloudException(title, message.format(name))

    def set_main_folder(self, path: str):
        """Setup your main folder"""
        edit_config("FCLOUD", "main_folder", path)

    def set_cfl_ex(self, extension: str):
        """Setup your cfl_extension"""
        edit_config("FCLOUD", "cfl_extension", extension)

    def set_parametr(self, section: str, parametr_name: str, value: str):
        "Set amy parametr to configuration"
        edit_config(section, parametr_name, value)

    def path(self):
        """Config path"""
        return self._path

    def read(self) -> str:
        """Text of the config file"""
        with open(self._path, "r") as config:
            return config.read()
