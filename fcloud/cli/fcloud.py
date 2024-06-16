import os
import contextlib
from pathlib import Path

from typing import Optional

from prettytable import PrettyTable
from dropbox.files import FileMetadata
from dropbox.files import FolderMetadata

from ..models.settings.settings import AuthData
from .protocol import FcloudProtocol
from .protocol import SomeStr

from ..utils.error import echo_error
from ..utils.cfl import create_cfl
from ..utils.cfl import delete_cfl
from ..utils.cfl import read_cfl

from .groups.config import Config
from ..exceptions.cfl_errors import CFLError
from ..exceptions.drivers_errors.drivers_exceptions import DriverException
from ..drivers.base import CloudProtocol


class Fcloud(FcloudProtocol):
    """
    Fcloud is a simple utility that makes it easy to work with the cloud.
    When synchronising, your files remain on your system
    with the file structure intact and your data is stored in the cloud.
    """

    def __init__(
        self,
        auth: AuthData,
        main_folder: Path,
        service: CloudProtocol,
        cfl_extension: str,
        available_clouds: list[str],
        without_driver: bool = False,
    ):
        """
        Args:
            auth (AuthData): Dataclass that stores cloud authorisation data in it
            main_folder (Path): Folder path for saving files on the cloud
            service (CloudProtocol): Driver class
            cfl_extension (str): Default extension for cfl files
            available_clouds (list[str]): List of supported cloud storage
            without_driver (bool, optional): Use if necessary to ignore the cloud
              connection. For example for tests, --help, etc. Defaults to False.
        """
        self.config = Config(available_clouds)
        try:
            if not without_driver:
                self._driver: CloudProtocol = service(auth, main_folder)
        except DriverException as er:
            echo_error((er.title, er.message))

        self._auth: AuthData = auth
        self._main_folder: Path = main_folder
        self._cfl_extension = cfl_extension

    def _to_path(self, path: SomeStr) -> Path:
        return Path(str(path))

    def _to_remote_path(self, path: SomeStr) -> Path:
        return self._main_folder if path is None else self._to_path(path)

    def add(
        self,
        path: Path,
        near: bool = False,
        filename: Optional[str] = None,
        remote_path: Optional[Path] = None,
        without_animation: bool = False,
    ) -> None:
        """Uploud file to cloud. More: https://fcloud.tech/docs/usage/commands/#add
        Args:
            -p --path (Path): Local path to file
            -n --near (bool, optional): Create cloud file link
              (cfl) near main file. Defaults to False.
            -f --filename (str, optional): Under which name the
              file will be saved in the cloud. Default is
              the name of the file on the local computer
            -r --remote_path (Path, optional): The folder under
              which the file will be uploaded to the server.
              Defaults to main folder from config.
            -w --without_animtaion (bool, Optional): Removes the
              loading animation. Default to False
        """
        p = Path(path := str(path))
        remote_path = self._to_remote_path(remote_path)

        if p.is_dir() and near:
            echo_error(CFLError.near_with_folder_error)
        elif p.is_dir():
            for file in [x for x in p.rglob("*") if x.is_file()]:
                with contextlib.suppress(SystemExit):
                    self.add(
                        file,
                        remote_path=remote_path,
                        without_animation=without_animation,
                    )
            return
        elif path[-len(self._cfl_extension) :] == self._cfl_extension:
            return
        elif not os.path.exists(p):
            echo_error(CFLError.not_exists_cfl_error)

        if filename is None:
            filename = os.path.basename(p)
        try:
            cloud_filename = self._driver.upload_file(
                p,
                filename=filename,
                remote_path=remote_path,
                without_anremote_pathimation=without_animation,
            )
        except DriverException as er:
            echo_error((er.title, er.message))

        create_cfl(path, cloud_filename, self._main_folder, self._cfl_extension, near)

    def get(
        self,
        cfl: SomeStr,
        near: bool = False,
        remove_after: bool = True,
        without_animation: bool = False,
    ) -> None:
        """Get file from cloud. More: https://fcloud.tech/docs/usage/commands/#get

        Args:
            -c --cfl (Path): File link to a file in the cloud,
              generated using <fcloud add ...>
            -n --near (bool, optiArgs:
            -c --cfl (Path):  File-link path
            -o --only_in_cloud (bool, optional): If true, will
              not delete cfl. Defaults to False.onal): Downloads a file without
              overwriting the link file. Defaults to False.
            -r --remove-after (bool, Optional): Deletes the file
              in the cloud after downloading. Default to False
            -w --without_animtaion (bool, Optional): Removes the
              loading animation. Default to False
        """
        cfl = self._to_path(cfl)
        cfl_ex = self._cfl_extension

        if cfl.is_file():
            path = read_cfl(cfl)
        elif cfl.is_dir():
            for file in [x for x in cfl.rglob("*") if x.is_file()]:
                with contextlib.suppress(SystemExit):
                    self.get(
                        file,
                        remove_after=remove_after,
                        without_animation=without_animation,
                    )
            return
        else:
            echo_error(CFLError.not_exists_cfl_error)

        if not near:
            try:
                self._driver.download_file(
                    path.name,
                    cfl,
                    path.parent,
                    without_animation=without_animation,
                )
            except DriverException as er:
                echo_error((er.title, er.message))

            if str(cfl).endswith(cfl_ex):
                new_name = cfl.name[: -len(cfl_ex)] if -len(cfl_ex) != 0 else cfl.name
                os.rename(cfl, cfl.parent / new_name)
        else:
            remove_after = False
            try:
                self._driver.download_file(
                    path.name,
                    cfl.parent / cfl.name[: -len(cfl_ex)],
                    path.parent,
                    without_animataion=False,
                )
            except DriverException as er:
                echo_error((er.title, er.message))

        if remove_after:
            try:
                self._driver.remove_file(path.name, path.parent)
            except DriverException as er:
                echo_error((er.title, er.message))

    def info(
        self,
        cfl: SomeStr,
    ) -> dict:
        """Info about file. More: https://fcloud.tech/docs/usage/commands/#info

        Args:
            -c --cfl (Path): File-link path
        """
        path = self._to_path(cfl)
        try:
            metadata = self._driver.info(read_cfl(path))
        except DriverException as er:
            echo_error((er.title, er.message))

        return {
            "Path": metadata.path_display,
            "Modified": metadata.server_modified,
            "Size": f"{metadata.size}B",
            "Content_hash": metadata.content_hash,
        }

    def remove(
        self,
        cfl: SomeStr,
        only_in_cloud: bool = False,
    ) -> None:
        """Will delete a file in the cloud by cfl. More: https://fcloud.tech/docs/usage/commands/#remove

        Args:
            -c --cfl (Path):  File-link path
            -o --only_in_cloud (bool, optional): If true, will
              not delete cfl. Defaults to False.
        """
        path = self._to_path(cfl)

        if path.is_file():
            remote_path = read_cfl(path)
            try:
                self._driver.remove_file(
                    remote_path.name,
                    remote_path.parent,
                )
            except DriverException as er:
                echo_error((er.title, er.message))

            if not only_in_cloud:
                delete_cfl(cfl)
        elif path.is_dir():
            for file in (x for x in path.rglob("*") if x.is_file()):
                with contextlib.suppress(SystemExit):
                    self.remove(file, only_in_cloud=only_in_cloud)
        else:
            echo_error(CFLError.not_exists_cfl_error)

    def files(
        self,
        remote_path: Optional[Path] = None,
        only_files: bool = False,
        without_animation: bool = False,
    ) -> PrettyTable:
        """Get info about all files. More: https://fcloud.tech/docs/usage/commands/#files

        Args:
            -r --remote_path (Path, optional): You have the option
              of specifying a custom folder for file information.
              Defaults to None.
            -o --only_files (bool, optional): Display only files in
              the output, ignoring folders. Defaults to False.
            -w --without_animtaion (bool, Optional): Removes the
              loading animation. Default to False
        """
        remote_path = self._to_remote_path(remote_path)
        if not only_files:
            columns = ["Filename", "Size", "Is_directory", "Modified"]
        else:
            columns = ["Filename", "Size", "Modified"]

        files_table = PrettyTable(
            columns,
            encoding="utf-8",
            title=f"Files in {remote_path}",
        )
        try:
            files: list[FileMetadata | FolderMetadata] = self._driver.get_all_files(
                Path("/" + str(remote_path)), without_animation=without_animation
            )
        except DriverException as er:
            echo_error((er.title, er.message))

        for file in files:
            if isinstance(file, FileMetadata) and only_files:
                files_table.add_row([file.name, file.size, file.server_modified])
            elif isinstance(file, FileMetadata):
                files_table.add_row([file.name, file.size, False, file.server_modified])
            elif isinstance(file, FolderMetadata) and not only_files:
                files_table.add_row([file.name, None, True, None])

        return files_table
