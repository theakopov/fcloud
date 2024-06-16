from pathlib import Path

from prettytable import PrettyTable

from typing import Protocol
from typing import TypeVar
from typing import Optional

from ..models.settings.settings import AuthData
from ..drivers.base import CloudProtocol

# Data received from the user that Fire
# can convert to another data type
# `script 1.1 hello` -> handler(float, str)
SomeStr = TypeVar("SomeStr", str, bytes, int, float)


class FcloudProtocol(Protocol):
    """
    A simple client for sending files to the cloud.
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
        wihtout_driver: bool = False,
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
        pass

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
        pass

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
        pass

    def info(
        self,
        cfl: SomeStr,
    ) -> dict:
        """Info about file. More: https://fcloud.tech/docs/usage/commands/#info

        Args:
            -c --cfl (Path): File-link path
        """
        pass

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
        pass

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
        pass
