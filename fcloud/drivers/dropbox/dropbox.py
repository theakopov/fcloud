from pathlib import Path
from typing import Callable
from typing import Optional

import dropbox
from dropbox.files import UploadSessionCursor
from dropbox.files import CommitInfo
from dropbox.files import Metadata
from dropbox.exceptions import AuthError
from dropbox.exceptions import BadInputError
from dropbox.dropbox_client import BadInputException
from dropbox.exceptions import ApiError
from dropbox.exceptions import HttpError
from stone.backends.python_rsrc.stone_validators import ValidationError


from requests import ConnectionError

from ...exceptions.file_errors import FileError
from ..base import CloudProtocol
from .errors import DropboxError
from .errors import DropboxException

from ...utils.other import generate_new_name


from .models import DropboxAuth


class DropboxCloud(CloudProtocol):
    def __init__(self, auth: DropboxAuth, main_folder: Path):
        self.chunk_size = 4 * 1024 * 1024
        self._main_folder = main_folder
        self._auth = auth
        self.app: dropbox.Dropbox = self.__exec(
            dropbox.Dropbox,
            oauth2_refresh_token=self._auth.token,
            app_key=self._auth.app_key,
            app_secret=self._auth.app_secret,
        )
        self.__exec(self.app.check_app)

    @staticmethod
    def __exec(func: Callable, *args, catch_unknown: bool = True, **kwargs):
        """Executes a request to the cloud api, handling standard errors
        Args:
            func (callable): api function
            catch_unknown (boolean): handles unknown errors from api, defaults - True

        Returns:
           Function execution result or raise error is not included in standard API errors
        """
        try:
            result = func(*args, **kwargs)
            return result
        except AuthError:
            raise DropboxException(DropboxError.auth_error)
        except BadInputError as er:
            title, message = DropboxError.badinput_error
            raise DropboxException((title, message.format(er.message)))
        except BadInputException as er:
            title, message = DropboxError.uncorrect_data_error
            raise DropboxException((title, message.format(er)))
        except HttpError:
            raise DropboxError(DropboxError.max_retries_error)
        except ApiError as er:
            raise DropboxException(("API error", er.args[1]))
        except ConnectionError:
            raise DropboxException(DropboxError.connection_error)
        except ValidationError:
            raise DropboxException(DropboxError.validation_error)
        except PermissionError:
            raise DropboxException(FileError.perrmission_denied)
        except Exception as er:
            if catch_unknown:
                title, message = DropboxError.uknown_error
                raise DropboxException((title.format(er), message.format(er)))
            raise

    def download_file(self, name: str, local_path: Path, remote_path: Path) -> None:
        self.__exec(
            self.app.files_download_to_file,
            local_path.as_posix(),
            (remote_path / Path(name)).as_posix(),
            catch_unknown=False,
        )

    def upload_file(self, local_path: Path, remote_path: Path, filename: str) -> str:
        files = [file.name for file in self.__exec(self.get_all_files, remote_path)]
        if filename in files:
            filename = generate_new_name(busy=files, default=filename)

        upload_session = self.__exec(self.app.files_upload_session_start, b"")
        cursor = self.__exec(
            UploadSessionCursor, session_id=upload_session.session_id, offset=0
        )
        try:
            with open(local_path, "rb") as file:
                while (data := file.read(self.chunk_size)) != b"":
                    self.__exec(self.app.files_upload_session_append_v2, data, cursor)
                    cursor.offset += len(data)

            commit = self.__exec(CommitInfo, path=(remote_path / filename).as_posix())
            self.__exec(self.app.files_upload_session_finish, b"", cursor, commit)
            return filename
        except FileNotFoundError:
            raise DropboxException(FileError.not_exists_error)
        except PermissionError:
            raise DropboxException(FileError.perrmission_denied)

    def get_all_files(self, remote_path: Path) -> list[Metadata]:
        files = self.__exec(self.app.files_list_folder, remote_path.as_posix()).entries

        return files

    def remove_file(self, filename: str, remote_path: Optional[Path] = None):
        self.__exec(self.app.files_delete, (remote_path / filename).as_posix())

    def info(self, path: Path) -> Metadata:
        return self.__exec(self.app.files_get_metadata, path.as_posix())
