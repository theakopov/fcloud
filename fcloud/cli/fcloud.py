import os
import contextlib
from pathlib import Path

from typing import Optional

from prettytable import PrettyTable
from dropbox.files import FileMetadata
from dropbox.files import FolderMetadata

from ..models.driver import T
from ..models.settings import Config as _Config
from .protocol import FcloudProtocol
from .protocol import SomeStr

from ..utils.error import echo_error
from ..utils.cfl import create_cfl
from ..utils.cfl import delete_cfl
from ..utils.cfl import read_cfl
from ..utils.animations import animation

from .groups.config import Config
from .groups.dropbox import Dropbox
from ..exceptions.cfl_errors import CFLError
from ..exceptions.driver_exceptions import DriverException
from ..drivers.base import CloudProtocol


class Fcloud(FcloudProtocol):
    """
    Fcloud is a simple utility that makes it easy to work with the cloud.
    When synchronising, your files remain on your system
    with the file structure intact and your data is stored in the cloud.
    """

    def __init__(
        self,
        available_clouds: list[str],
        config: Optional[_Config] = None,
        without_driver: bool = False,
    ):
        """
        Args:
            available_clouds (list[str]): List of supported cloud storage
            config (_Config, optional): Dataclass containing: service (driver name),
              main_folder, cloud authorization data, cfl_extension
            without_driver (bool, optional): Use if necessary to ignore the cloud
              connection. For example for tests, --help, etc. Defaults to False.
        """
        # init subcommands `fcloud config`, `fcloud dropbox` ...
        self.config = Config(available_clouds)
        self.dropbox = Dropbox()

        if without_driver:
            return

        try:
            self._driver: CloudProtocol = config.service.driver(
                config.service.auth_model, config.main_folder
            )
        except DriverException as er:
            echo_error((er.title, er.message))

        self._auth: T = config.service.auth_model
        self._main_folder: Path = config.main_folder
        self._cfl_extension = config.cfl_extension

    def _to_path(self, path: SomeStr) -> Path:
        return Path(str(path))

    def _to_remote_path(self, path: SomeStr) -> Path:
        return self._main_folder if path is None else self._to_path(path)

    @animation("Uploading")
    def add(
        self,
        path: Path,
        near: bool = False,
        filename: Optional[str] = None,
        remote_path: Optional[Path] = None,
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
                        without_animation=True,
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
            )
        except DriverException as er:
            echo_error((er.title, er.message))

        create_cfl(path, cloud_filename, self._main_folder, self._cfl_extension, near)

    @animation("Downloading")
    def get(self, cfl: SomeStr, near: bool = False, remove_after: bool = True) -> None:
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
                        without_animation=True,
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
                )
            except DriverException as er:
                echo_error((er.title, er.message))

        if remove_after:
            try:
                self._driver.remove_file(path.name, path.parent)
            except DriverException as er:
                echo_error((er.title, er.message))

    @animation("Information collection")
    def info(self, cfl: SomeStr) -> dict:
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

    def remove(self, cfl: SomeStr, only_in_cloud: bool = False) -> None:
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

    @animation("Collecting files")
    def files(
        self, remote_path: Optional[Path] = None, only_files: bool = False
    ) -> PrettyTable:
        """Get info about all files. More: https://fcloud.tech/docs/usage/commands/#files

        Args:
            -r --remote_path (Path, optional): You have the option
              of specifying a custom folder for file information.
              Defaults to None.
            -o --only_files (bool, optional): Display only files in
              the output, ignoring folders. Defaults to False.
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
                Path("/" + str(remote_path))
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
