import configparser
import os
from pathlib import Path
from typing import Optional

from .exceptions.config_errors import ConfigError
from .exceptions.driver_errors import DriverError
from .exceptions.exceptions import FcloudConfigException

from .models.settings import Config
from .models.driver import Driver

from .utils.config import get_field
from .utils.config import get_section


def _service_validator(service: str, drivers: list[Driver]) -> str:
    service = service.lower()
    if service not in [x.name for x in drivers]:
        title, message = DriverError.driver_error
        raise FcloudConfigException(title, message.format(service))
    return service


def _main_folder_validator(main_folder: str) -> Path:
    if not (main_folder.startswith("/") or main_folder.startswith("\\")):
        main_folder = "/" + main_folder
    folder = Path(main_folder).as_posix()
    return Path(folder)


def _driver_init(service: str, drivers: list[Driver], initial_settings):
    driver = [d for d in drivers if d.name == service][0]
    driver.auth_model = driver.auth_model(**initial_settings)
    return driver


def read_config(drivers: list[Driver], path: Optional[Path] = None) -> Config:
    if path is None:
        path = Path(os.environ.get("FCLOUD_CONFIG_PATH"))

    if not path.exists():
        raise FcloudConfigException(*ConfigError.config_not_found)

    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")

    fields = {
        "service": "",
        "cfl_extension": "",
        "main_folder": "",
    }
    for field in fields:
        title, message = ConfigError.field_error
        message.format(field, os.environ["FCLOUD_CONFIG_PATH"])
        fields[field] = get_field(field, (title, message), config)

    fields["service"] = _service_validator(fields["service"], drivers)
    fields["main_folder"] = _main_folder_validator(fields["main_folder"])

    cloud_settings = get_section(
        fields["service"].upper(), ConfigError.section_error, config
    )

    for key, value in (fields | dict(cloud_settings)).items():
        section = fields["service"] if key in cloud_settings else "FCLOUD"
        if value == "" or value == ".":
            title, message = ConfigError.field_emty_error
            raise FcloudConfigException(title.format(key), message.format(section, key))

    fields["service"] = _driver_init(fields["service"], drivers, cloud_settings)

    return Config(**fields)
