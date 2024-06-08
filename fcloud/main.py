import os
import sys
from pathlib import Path

from art import tprint
from fire import Fire

from .config import read_config
from .models.drivers.drivers import Drivers
from .cli.groups.config import Config
from .cli.fcloud import Fcloud


def main():
    if os.environ.get(env := "FCLOUD_CONFIG_PATH") is None:
        path = Path(os.path.abspath(__file__)).parent / Path(".conf")
        os.environ[env] = str(path)
    else:
        path = Path(os.environ.get(env))

    available_clouds = ["dropbox"]
    if len(sys.argv) == 1:
        tprint("FCLOUD")
    elif sys.argv[1] == "config":
        Fire(Config(available_clouds, path), sys.argv[2:], "fcloud config")
    else:
        config = read_config(available_clouds, path)
        driver = Drivers[config.service.lower()].value
        cli = Fcloud(
            auth=config.auth,
            main_folder=config.main_folder,
            service=driver,
            cfl_extension=config.cfl_extension,
            available_clouds=available_clouds,
        )
        Fire(cli, name="fcloud")
