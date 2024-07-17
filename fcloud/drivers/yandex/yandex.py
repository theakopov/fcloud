import os
from yadisk import Client

from pathlib import Path
from typing import Callable
from functools import wraps

from ..base import CloudProtocol
from .models import YandexAuth
from ...utils.other import generate_new_name


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

        self._app = Client(auth.client_id, auth.client_secret, auth.token)

    def download_file(self, path: Path, local_path: Path) -> None:
        self._app.download(str(path), str(local_path))

    def upload_file(self, local_path: Path, path: Path) -> str:
        filename = os.path.basename(path)
        self.get_all_files(path.parent)
        files = [file.name for file in self.get_all_files(path.parent)]
        if filename in files:
            filename = generate_new_name(busy=files, default=filename)
        self._app.upload(str(local_path), str(path))

        return filename

    def get_all_files(self, remote_path: Path) -> list:
        return list(self._app.listdir(str(remote_path)))

    def remove_file(self, path: Path) -> None:
        self._app.remove(str(path))

    def info(self, path: Path) -> dict:
        metadata = self._app.get_meta(str(path))
        return {
            "Path": metadata.path,
            "Size": f"{metadata.size} B",
            "Media type": metadata.media_type,
            "Content hash": metadata.md5,
            "Modified": metadata.modified,
            "Antivirus status": metadata.antivirus_status,
        }
