from yadisk import Client

from pathlib import Path
from typing import Callable
from functools import wraps

from ..base import CloudProtocol

from .models import YandexAuth


def catch_api_error(func: Callable):
    """A decorator that catches errors from the
      Dropbox api and prints them to the user

    Args:
        func (Callable): driver method
    """

    @wraps(func)
    def inner(*args, **kwargs):
        pass

    return inner


class YandexCloud(CloudProtocol):
    def __init__(self, auth: YandexAuth, main_folder: Path):
        self._main_folder = main_folder
        self._auth = auth

        self.app = Client(auth.client_id, auth.client_secret, auth.token)
        self.app.check_token()

    def download_file(self, path: Path, local_path: Path) -> None:
        pass

    def upload_file(self, local_path: Path, path: Path) -> str:
        pass

    def get_all_files(self, remote_path: Path) -> list:
        pass

    def remove_file(self, path: Path) -> None:
        pass

    def info(self, path: Path) -> dict:
        pass
