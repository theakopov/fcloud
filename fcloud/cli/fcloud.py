import os
import fire
import contextlib
from pathlib import Path
from textwrap import dedent
from typing import Optional
from typing import Generic


from prettytable import PrettyTable

from ..models.driver import T
from ..models.driver import Driver
from ..models.settings import Config as _Config
from ..models.settings import CloudObj
from ..models.settings import UserArgument

from ..utils.cfl import create_cfl
from ..utils.cfl import delete_cfl
from ..utils.cfl import read_cfl
from ..utils.animations import animation

from .groups.config import Config
from .groups.dropbox import Dropbox
from .groups.yandex import Yandex

from ..drivers.base import CloudProtocol
from ..exceptions.cfl_errors import CFLError
from ..exceptions.file_errors import FileError
from ..exceptions.config_errors import ConfigError
from ..exceptions.exceptions import FcloudException


class Fcloud:
    """
    Fcloud is a simple utility that makes it easy to work with the cloud.
    When synchronising, your files remain on your system
    with the file structure intact and your data is stored in the cloud.
    """

    def __init__(
        self,
        drivers: list[Driver],
        config: _Config | None,
    ):
        """
        Args:
            drivers (list[Driver]): List of supported cloud storage
            config (_Config, optional): Dataclass containing: service (driver name),
              main_folder, cloud authorization data, cfl_extension
            with_driver (bool, optional): Use when you need to connect to the cloud.
              For example, for tests, --help, etc., use False. The default value is True.
        """
        # init subcommands `fcloud config`, `fcloud dropbox` ...
        self.config = Config([x.name for x in drivers])
        self.dropbox = Dropbox()
        self.yandex = Yandex()

        if config is None:
            return

        service = [d for d in drivers if d.name == config.service][0]
        try:
            auth = service.auth_model(**config.section_fields)
        except TypeError:
            raise FcloudException(*ConfigError.section_error)

        self._driver: CloudProtocol = service.driver(auth, config.main_folder)
        self._auth: Generic[T] = auth
        self._main_folder: Path = config.main_folder
        self._cfl_extension = config.cfl_extension

    def __call__(self, *args, **kwargs):
        if args or kwargs:
            fire.Fire(object, name="fcloud")

        print(
            dedent("""\
                 _____   ____  _       ___   _   _  ____  
                |  ___| / ___|| |     / _ \ | | | ||  _ \ 
                | |_   | |    | |    | | | || | | || | | |
                |  _|  | |___ | |___ | |_| || |_| || |_| |
                |_|     \____||_____| \___/  \___/ |____/                                   
                """)
        )

    def _to_path(self, path: UserArgument) -> Path:
        return Path(str(path))

    def _to_remote_path(self, path: UserArgument | None) -> Path:
        return self._main_folder if path is None else self._to_path(path)

    @animation("Uploading")
    def add(
        self,
        path: UserArgument,
        near: bool = False,
        filename: Optional[UserArgument] = None,
        remote_path: Optional[UserArgument] = None,
    ) -> None:
        """Uploud file to cloud. More: https://fcloud.tech/docs/usage/commands/#add
        Args:
            -p --path (UserArgument): Local path to file
            -n --near (bool, optional): Create cloud file link
              (cfl) near main file. Defaults to False.
            -f --filename (UserArgument, optional): Under which name the
              file will be saved in the cloud. Default is
              the name of the file on the local computer
            -r --remote_path (UserArgument, optional): The folder under
              which the file will be uploaded to the server.
              Defaults to main folder from config.
        """
        lremote_path = self._to_remote_path(remote_path)
        lpath = self._to_path(path)

        if lpath.is_dir() and near:
            raise FcloudException(*CFLError.near_with_folder_error)
        elif not lpath.exists():
            raise FcloudException(*FileError.not_exists_error)
        elif str(lpath)[-len(self._cfl_extension) :] == self._cfl_extension:
            return

        if lpath.is_dir():
            for file in [x for x in lpath.rglob("*") if x.is_file()]:
                with contextlib.suppress(SystemExit):
                    self.add(
                        str(file),
                        remote_path=lremote_path,
                        without_animation=True,
                    )
            return

        if filename is None:
            lfilename = Path(os.path.basename(lpath))
        else:
            lfilename = Path(str(filename))

        cloud_filename = self._driver.upload_file(lpath, lremote_path / lfilename)

        create_cfl(lpath, cloud_filename, lremote_path, self._cfl_extension, near)

    @animation("Downloading")
    def get(
        self,
        cfl: UserArgument,
        near: bool = False,
        remove_after: bool = True,
    ) -> None:
        """Get file from cloud. More: https://fcloud.tech/docs/usage/commands/#get

        Args:
            -c --cfl (UserArgument): File link to a file in the cloud,
              generated using <fcloud add ...>
            -n --near (bool, optional): Downloads a file without
              overwriting the link file. Defaults to False.
            -o --only_in_cloud (bool, optional): If true, will
              not delete cfl. Defaults to False)
            -r --remove-after (bool, Optional): Deletes the file
              in the cloud after downloading. Default to False
        """
        lcfl = self._to_path(cfl)
        cfl_ex = self._cfl_extension

        if lcfl.is_file():
            path = read_cfl(lcfl)
        elif lcfl.is_dir():
            for file in [x for x in lcfl.rglob("*") if x.is_file()]:
                with contextlib.suppress(SystemExit):
                    self.get(
                        str(file),
                        remove_after=remove_after,
                        without_animation=True,
                    )
            return
        else:
            raise FcloudException(*CFLError.not_exists_cfl_error)

        if not near:
            self._driver.download_file(path, lcfl)

            if str(lcfl).endswith(cfl_ex):
                new_name = lcfl.name[: -len(cfl_ex)] if -len(cfl_ex) != 0 else lcfl.name
                os.rename(lcfl, lcfl.parent / new_name)
        else:
            remove_after = False
            self._driver.download_file(path, lcfl.parent / lcfl.name[: -len(cfl_ex)])

        if remove_after:
            self._driver.remove_file(path)

    @animation("Information collection")
    def info(self, cfl: UserArgument) -> dict:
        """Info about file. More: https://fcloud.tech/docs/usage/commands/#info

        Args:
            -c --cfl (UserArgument): File-link path
        """
        lcfl = self._to_path(cfl)
        return self._driver.info(read_cfl(lcfl))

    def remove(self, cfl: UserArgument, only_in_cloud: bool = False) -> None:
        """Will delete a file in the cloud by cfl. More: https://fcloud.tech/docs/usage/commands/#remove

        Args:
            -c --cfl (UserArgument):  File-link path
            -o --only_in_cloud (bool, optional): If true, will
              not delete cfl. Defaults to False.
        """
        lcfl = self._to_path(cfl)

        if lcfl.is_file():
            remote_path = read_cfl(lcfl)
            self._driver.remove_file(remote_path)

            if not only_in_cloud:
                delete_cfl(lcfl)
        elif lcfl.is_dir():
            for file in (x for x in lcfl.rglob("*") if x.is_file()):
                with contextlib.suppress(SystemExit):
                    self.remove(str(file), only_in_cloud=only_in_cloud)
        else:
            raise FcloudException(*CFLError.not_exists_cfl_error)

    @animation("Collecting files")
    def files(
        self, remote_path: Optional[UserArgument] = None, only_files: bool = False
    ) -> PrettyTable:
        """Get info about all files. More: https://fcloud.tech/docs/usage/commands/#files

        Args:
            -r --remote_path (UserArgument, optional): You have the option
              of specifying a custom folder for file information.
              Defaults to None.
            -o --only_files (bool, optional): Display only files in
              the output, ignoring folders. Defaults to False.
        """
        lremote_path = self._to_remote_path(remote_path)

        if not only_files:
            columns = ["Filename", "Size", "Is_directory", "Modified"]
        else:
            columns = ["Filename", "Size", "Modified"]

        files_table = PrettyTable(
            columns, encoding="utf-8", title=f"Files in {lremote_path}"
        )
        files: list[CloudObj] = self._driver.get_all_files(lremote_path)

        for file in files:
            if not file.is_directory and only_files:
                files_table.add_row([file.name, file.size, file.modifed])
            elif not file.is_directory:
                files_table.add_row([file.name, file.size, False, file.modifed])
            elif file.is_directory and not only_files:
                files_table.add_row([file.name, None, True, None])

        return files_table
