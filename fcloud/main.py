import os
import sys
from pathlib import Path

from art import tprint
from fire import Fire

from .config import read_config
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
        return

    sub_command = sys.argv[1] in ["config", *available_clouds]
    without_driver = sub_command or "--help" in sys.argv
    if not without_driver:
        config = read_config(available_clouds, path)
    else:
        config = None

    cli = Fcloud(
        available_clouds=available_clouds,
        config=config,
        without_driver=without_driver,
    )

    Fire(cli, name="fcloud")
