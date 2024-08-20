import os
from pathlib import Path
from typing import Callable
from functools import wraps

import dropbox
from dropbox.dropbox_client import BadInputException
from dropbox.files import UploadSessionCursor
from dropbox.files import CommitInfo
from dropbox.files import Metadata
from dropbox.files import FileMetadata
from dropbox.files import FolderMetadata
from dropbox.exceptions import AuthError
from dropbox.exceptions import BadInputError
from dropbox.exceptions import ApiError
from dropbox.exceptions import HttpError
from requests.exceptions import ProxyError
from stone.backends.python_rsrc.stone_validators import ValidationError


from requests import ConnectionError

from ...models.settings import CloudObj
from ...exceptions.file_errors import FileError
from ..base import CloudProtocol
from .errors import DropboxError
from .errors import DropboxException

from ...utils.other import generate_new_name


from .models import DropboxAuth


def dropbox_api_error(func: Callable):
    """A decorator that catches errors from the
      Dropbox api and prints them to the user

    Args:
        func (Callable): driver method
    """

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except AuthError:
            raise DropboxException(*DropboxError.auth_error)
        except BadInputError as er:
            title, message = DropboxError.badinput_error
            raise DropboxException(title, message.format(er.message))
        except BadInputException as er:
            title, message = DropboxError.uncorrect_data_error
            raise DropboxException(title, message.format(er))
        except (HttpError, ProxyError):
            raise DropboxException(*DropboxError.max_retries_error)
        except ApiError as er:
            raise DropboxException("API error", er.args[1])
        except ConnectionError:
            raise DropboxException(*DropboxError.connection_error)
        except ValidationError:
            raise DropboxException(*DropboxError.validation_error)
        except FileNotFoundError:
            raise DropboxException(*FileError.not_exists_error)
        except PermissionError:
            raise DropboxException(*FileError.perrmission_denied)
        except Exception as er:
            title, message = DropboxError.uknown_error
            raise DropboxException(title.format(er), message.format(er))

    return inner


class DropboxCloud(CloudProtocol):
    @dropbox_api_error
    def __init__(self, auth: DropboxAuth, main_folder: Path):
        self.chunk_size = 4 * 1024 * 1024
        self._main_folder = main_folder
        self._auth = auth
        self.app: dropbox.Dropbox = dropbox.Dropbox(
            oauth2_refresh_token=self._auth.token,
            app_key=self._auth.app_key,
            app_secret=self._auth.app_secret,
        )
        self.app.check_app()

    @dropbox_api_error
    def download_file(self, path: Path, local_path: Path) -> None:
        self.app.files_download_to_file(local_path.as_posix(), path.as_posix())

    @dropbox_api_error
    def upload_file(self, local_path: Path, path: Path) -> str:
        try:
            self.app.files_get_metadata(str(path))
        except ApiError:
            raise ApiError(*DropboxError.path_not_found_error, None, None)

        filename = os.path.basename(path)
        files = [file.name for file in self.get_all_files(path.parent)]
        if filename in files:
            filename = generate_new_name(busy=files, default=filename)

        upload_session = self.app.files_upload_session_start(b"")
        cursor = UploadSessionCursor(session_id=upload_session.session_id, offset=0)
        with open(local_path, "rb") as file:
            while (data := file.read(self.chunk_size)) != b"":
                self.app.files_upload_session_append_v2(data, cursor)
                cursor.offset += len(data)

        commit = CommitInfo(path=path.as_posix())
        self.app.files_upload_session_finish(b"", cursor, commit)
        return filename

    @dropbox_api_error
    def get_all_files(self, remote_path: Path) -> list[Metadata]:
        files = []
        for cloud_obj in self.app.files_list_folder(remote_path.as_posix()).entries:
            if isinstance(cloud_obj, FileMetadata):
                files.append(
                    CloudObj(
                        name=cloud_obj.name,
                        size=cloud_obj.size,
                        is_directory=False,
                        modifed=cloud_obj.server_modified,
                    )
                )
            elif isinstance(cloud_obj, FolderMetadata):
                files.append(
                    CloudObj(
                        name=cloud_obj.name,
                        size=None,
                        is_directory=True,
                        modifed=None,
                    )
                )
        return files

    @dropbox_api_error
    def remove_file(self, path: Path):
        self.app.files_delete(path.as_posix())

    @dropbox_api_error
    def info(self, path: Path) -> dict:
        metadata = self.app.files_get_metadata(path.as_posix())

        return {
            "Path": metadata.path_display,
            "Modified": metadata.server_modified,
            "Size": f"{metadata.size}B",
            "Content hash": metadata.content_hash,
        }
