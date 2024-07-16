import os
import sys
from pathlib import Path

from fire import Fire

from .config import read_config
from .cli.fcloud import Fcloud
from .models.driver import Driver
from .utils.error import catch_error

from .drivers.dropbox.dropbox import DropboxCloud
from .drivers.dropbox.models import DropboxAuth

from .drivers.yandex.yandex import YandexCloud
from .drivers.yandex.models import YandexAuth


@catch_error
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
        ),
        Driver(
            name="yandex",
            driver=YandexCloud,
            auth_model=YandexAuth,
        ),
    ]

    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    _help = "--help" in sys.argv
    with_driver = not (cmd in ["config", None, *[x.name for x in drivers]] or _help)

    cli = Fcloud(
        available_clouds=[x.name for x in drivers],
        config=read_config(drivers, path) if with_driver else None,
        with_driver=with_driver,
    )

    Fire(cli, name="fcloud")
