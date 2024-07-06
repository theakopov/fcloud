import configparser
import os
from pathlib import Path
from typing import Optional
from typing import NoReturn

from .exceptions.config_errors import ConfigError
from .exceptions.driver_errors import DriverError
from .exceptions.exceptions import FcloudConfigException

from .models.settings import Config
from .models.driver import Driver

from .utils.config import get_field


def not_empty(
    key: str, value: str, section: str = "FCLOUD", quit_afer: bool = True
) -> None | NoReturn:
    if not (value == "" or value == "."):
        return

    title, message = ConfigError.field_emty_error
    raise FcloudConfigException(title.format(key), message.format(section, key))


def read_config(drivers: list[Driver], path: Optional[Path] = None) -> Config:
    if path is None:
        path = os.environ.get("FCLOUD_CONFIG_PATH")

    if not path.exists():
        raise FcloudConfigException(ConfigError.config_not_found)
    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")

    # service
    cloud = get_field("service", error=ConfigError.service_error, config=config).lower()
    if cloud not in [x.name for x in drivers]:
        title, message = DriverError.driver_error
        raise FcloudConfigException(title, message.format(cloud))

    # cfl_extension
    cfl_extension = get_field("cfl_extension", ConfigError.cfl_extension_error, config)

    # main_folder
    main_folder = get_field("main_folder", ConfigError.main_folder_error, config)
    if not (main_folder.startswith("/") or main_folder.startswith("\\")):
        main_folder = "/" + main_folder
    main_folder = Path(main_folder).as_posix()

    # Section, for cloud storage settings
    cloud_settings = get_field(
        section=cloud.upper(), error=ConfigError.section_error, config=config
    )

    driver = [d for d in drivers if d.name == cloud][0]
    driver.auth_model = driver.auth_model(**cloud_settings)

    fields = {
        "service": cloud,
        "cfl_extension": cfl_extension,
        "main_folder": main_folder,
        **cloud_settings,
    }

    for key, value in fields.items():
        section = cloud if key in cloud_settings else "FCLOUD"
        not_empty(key, value, section.upper())

    return Config(
        service=driver,
        main_folder=Path(main_folder),
        cfl_extension=str(cfl_extension),
    )
