import configparser
import os
from pathlib import Path
from typing import Optional
from typing import NoReturn

from .exceptions.config_errors import ConfigError
from .exceptions.driver_errors import DriverError

from .models.settings import Config
from .models.settings import AuthData

from .utils.error import echo_error
from .utils.config import get_config_data


def not_empty(
    key: str, value: str, section: str = "FCLOUD", quit_afer: bool = True
) -> None | NoReturn:
    if not (value == "" or value == "."):
        return

    title, message = ConfigError.field_emty_error
    echo_error(
        (title.format(key), message.format(section, key)),
        need_to_quit=quit_afer,
    )


def read_config(available_clouds: list[str], path: Optional[Path] = None) -> Config:
    if path is None:
        path = os.environ.get("FCLOUD_CONFIG_PATH")

    if not path.exists():
        echo_error(ConfigError.config_not_found)
    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")

    # service
    cloud = get_config_data(
        "FCLOUD", "service", error=ConfigError.service_error, config=config
    ).lower()
    if cloud not in available_clouds:
        title, message = DriverError.driver_error
        echo_error((title, message.format(cloud)))

    # cfl_extension
    cfl_extension = get_config_data(
        "FCLOUD", "cfl_extension", error=ConfigError.cfl_extension_error, config=config
    )
    # main_folder
    main_folder = get_config_data(
        "FCLOUD", "main_folder", error=ConfigError.main_folder_error, config=config
    )
    if not (main_folder.startswith("/") or main_folder.startswith("\\")):
        main_folder = "/" + main_folder
    main_folder = Path(main_folder).as_posix()

    # Section, for cloud storage settings
    cloud_settings = get_config_data(
        cloud.upper(), error=ConfigError.section_error, config=config
    )

    auth_model = AuthData[cloud.lower()].value

    fields = {
        "service": cloud,
        "cfl_extension": cfl_extension,
        "main_folder": main_folder,
    }
    for key, value in (fields | dict(cloud_settings)).items():
        section = "FCLOUD" if key in fields else cloud
        not_empty(key, value, section.upper())

    return Config(
        service=cloud,
        main_folder=Path(main_folder),
        auth=auth_model(**cloud_settings),
        cfl_extension=str(cfl_extension),
    )
