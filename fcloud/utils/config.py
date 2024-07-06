import os
import configparser
from typing import Optional


from ..exceptions.config_errors import ConfigError
from ..exceptions.base_errors import FcloudError
from ..exceptions.exceptions import FcloudConfigException


def edit_config(section: str, name: str, value: str) -> None:
    path = os.environ.get("FCLOUD_CONFIG_PATH")
    config = configparser.ConfigParser()
    config.read(path)
    config[str(section)][str(name)] = str(value)
    try:
        with open(path, "w", encoding="utf-8") as configfile:
            config.write(configfile)
    except FileNotFoundError:
        raise FcloudConfigException(*ConfigError.config_not_found)
    except PermissionError:
        raise FcloudConfigException(*ConfigError.perrmission_denied)


def get_field(
    parameter: Optional[str] = None,
    error: tuple[str, str] = FcloudError.uknown_error,
    config: Optional[configparser.ConfigParser] = None,
    section: str = "FCLOUD",
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
        raise FcloudConfigException(*error)
