import os
import configparser
from typing import Optional

from .error import echo_error

from ..exceptions.config_errors import ConfigError
from ..exceptions.base_errors import FcloudError


def edit_config(section: str, name: str, value: str) -> None:
    path = os.environ.get("FCLOUD_CONFIG_PATH")
    config = configparser.ConfigParser()
    config.read(path)
    config[str(section)][str(name)] = str(value)
    try:
        with open(path, "w", encoding="utf-8") as configfile:
            config.write(configfile)
    except FileNotFoundError:
        echo_error(ConfigError.config_not_found)
    except PermissionError:
        echo_error(ConfigError.perrmission_denied)


def get_config_data(
    section: str,
    parameter: str = None,
    error: tuple[str, str] = FcloudError.uknown_error,
    config: Optional[configparser.ConfigParser] = None,
) -> str | dict | None:
    if not config:
        path = os.environ.get("FCLOUD_CONFIG_PATH")
        config = configparser.ConfigParser()
        config.read(path)

    try:
        if parameter is not None:
            return config[str(section)][str(parameter)]
        else:
            return config[str(section)]
    except KeyError:
        echo_error(error)
