import os
import sys
from pathlib import Path

from art import tprint
from fire import Fire

from .config import read_config
from .cli.fcloud import Fcloud
from .models.driver import Driver

from .drivers.dropbox.dropbox import DropboxCloud
from .drivers.dropbox.models import DropboxAuth


def main():
    if os.environ.get(env := "FCLOUD_CONFIG_PATH") is None:
        path = Path(os.path.abspath(__file__)).parent / Path(".conf")
        os.environ[env] = str(path)
    else:
        path = Path(os.environ.get(env))

    # Here you can add your own driver
    drivers = [
        Driver(
            name="dropbox",
            driver=DropboxCloud,
            auth_model=DropboxAuth,
        )
    ]
    if len(sys.argv) == 1:
        tprint("FCLOUD")
        return

    sub_command = sys.argv[1] in ["config", *[x.name for x in drivers]]
    without_driver = sub_command or "--help" in sys.argv
    if not without_driver:
        config = read_config(drivers, path)
    else:
        config = None

    cli = Fcloud(
        available_clouds=[x.name for x in drivers],
        config=config,
        without_driver=without_driver,
    )

    Fire(cli, name="fcloud")
