import configparser
import os
from pathlib import Path
from typing import Optional

from .exceptions.config_errors import ConfigError
from .exceptions.driver_errors import DriverError
from .exceptions.exceptions import FcloudConfigException

from .models.settings import Config
from .models.settings import Fields
from .models.driver import Driver

from .utils.config import get_field
from .utils.config import get_section


def _service_validator(service: str, drivers: list[Driver]) -> str:
    if service.lower() not in [x.name for x in drivers]:
        title, message = DriverError.driver_error
        raise FcloudConfigException(title, message.format(service))
    return service


def _main_folder_validator(main_folder: str) -> Path:
    if not (main_folder.startswith("/") or main_folder.startswith("\\")):
        main_folder = "/" + main_folder
    folder = Path(main_folder).as_posix()
    return Path(folder)


def read_config(drivers: list[Driver], path: Optional[Path] = None) -> Config:
    if path is None:
        path = Path(os.environ.get("FCLOUD_CONFIG_PATH"))

    if not path.exists():
        raise FcloudConfigException(*ConfigError.config_not_found)

    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")

    fields = {}
    for field in ("service", "main_folder", "cfl_extension"):
        title, message = ConfigError.field_error
        fields[field] = get_field(field, (title, message.format(field, path)), config)

    fld = Fields(**fields)
    fld.service = _service_validator(fld.service, drivers)
    fld.main_folder = _main_folder_validator(fld.main_folder)

    cloud_settings = get_section(fld.service, ConfigError.section_error, config)

    for key, value in cloud_settings.items():
        if value == "" or value == ".":
            title, message = ConfigError.field_emty_error
            raise FcloudConfigException(
                title.format(key), message.format(fld.service, key)
            )

    return Config(
        service=fld.service,
        main_folder=fld.main_folder,
        cfl_extension=fld.cfl_extension,
        section_fields=dict(cloud_settings),
    )
