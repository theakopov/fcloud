import os
from yadisk import Client

from pathlib import Path
from typing import Callable
from functools import wraps

from yadisk.exceptions import YaDiskConnectionError
from yadisk.exceptions import RequestTimeoutError
from yadisk.exceptions import PathNotFoundError
from yadisk.exceptions import UnauthorizedError

from .errors import YandexException
from .errors import YandexError

from .models import YandexAuth
from ..base import CloudProtocol
from ...models.settings import CloudObj
from ...utils.other import generate_new_name
from ...exceptions.file_errors import FileError


def yandex_api_error(func: Callable):
    """A decorator that catches errors from the
      Dropbox api and prints them to the user

    Args:
        func (Callable): driver method
    """

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except YaDiskConnectionError:
            raise YandexException(*YandexError.connection_error)
        except RequestTimeoutError:
            raise YandexException(*YandexError.timed_out_error)
        except PathNotFoundError:
            raise YandexException(*YandexError.path_not_found_error)
        except UnauthorizedError:
            raise YandexException(*YandexError.invalid_token_error)
        except FileNotFoundError:
            raise YandexException(*FileError.not_exists_error)
        except PermissionError:
            raise YandexException(*FileError.perrmission_denied)
        except Exception as er:
            title, message = YandexError.uknown_error
            raise YandexException(title.format(er), message.format(er))

    return inner


class YandexCloud(CloudProtocol):
    @yandex_api_error
    def __init__(self, auth: YandexAuth, main_folder: Path):
        self._main_folder = main_folder
        self._auth = auth
        self._app = Client(auth.client_id, auth.client_secret, auth.token)

        if not self._app.check_token():
            raise UnauthorizedError

    @yandex_api_error
    def download_file(self, path: Path, local_path: Path) -> None:
        self._app.download(str(path), str(local_path))

    @yandex_api_error
    def upload_file(self, local_path: Path, path: Path) -> str:
        filename = os.path.basename(path)
        if not self._app.exists(str(path.parent)):
            raise PathNotFoundError
        files = [file.name for file in self.get_all_files(path.parent)]
        if filename in files:
            filename = generate_new_name(files, filename)
        self._app.upload(str(local_path), str(path.parent.joinpath(filename)))

        return filename

    @yandex_api_error
    def get_all_files(self, remote_path: Path) -> list[CloudObj]:
        return [
            CloudObj(
                name=file.name,
                size=file.size,
                is_directory=file.media_type == "folder",
                modifed=file.modified,
            )
            for file in self._app.listdir(str(remote_path))
        ]

    @yandex_api_error
    def remove_file(self, path: Path) -> None:
        self._app.remove(str(path))

    @yandex_api_error
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
