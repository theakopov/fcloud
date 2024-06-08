import configparser
import os
from pathlib import Path
from typing import Optional

from .exceptions.config_errors.base_config_errors import ConfigError
from .exceptions.drivers_errors.base import DriverError

from .models.settings.settings import Config
from .models.settings.settings import AuthData

from .utils.error import echo_error
from .utils.config import get_config_data


def read_config(available_clouds: list[str], path: Optional[Path] = None) -> Config:
    if path is None:
        path = os.environ.get("FCLOUD_CONFIG_PATH")

    if not path.exists():
        echo_error(ConfigError.config_not_found)

    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")

    cloud = get_config_data(
        "FCLOUD", "service", error=ConfigError.service_error, config=config
    )
    if cloud not in available_clouds:
        title, message = DriverError.driver_error
        echo_error((title, message.format(cloud)))

    cloud_settings = get_config_data(
        cloud.upper(), error=ConfigError.section_error, config=config
    )

    cfl_extension = get_config_data("FCLOUD", "cfl_extension", config=config)

    main_folder = Path(
        get_config_data(
            "FCLOUD", "main_folder", error=ConfigError.main_folder_error, config=config
        )
    ).as_posix()

    auth_model = AuthData[cloud.lower()].value

    return Config(
        service=cloud,
        main_folder=Path(main_folder),
        auth=auth_model(**cloud_settings),
        cfl_extension=str(cfl_extension),
    )
