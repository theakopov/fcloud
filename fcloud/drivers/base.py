from typing import Protocol
from pathlib import Path


class CloudProtocol(Protocol):
    def __init__(self, auth, main_folder: Path):
        pass

    def download_file(
        self,
        name: str,
        local_path: Path,
        remote_path: Path,
    ) -> None:
        """Download a file from the cloud

        Args:
            name (str): File name in the cloud
            local_path (Path): The path where you want to save the downloaded file
            remote_path (Path): Path to the file in the cloud
        """
        pass

    def upload_file(
        self,
        local_path: Path,
        filename: str,
        remote_path: Path,
    ) -> str:
        """Upload a file to the cloud

        Args:
            local_path (Path): Path to the file to be uploaded
            filename (str): The name that will be assigned to the file in the cloud
            remote_path (Path): The path where you want to save the file in the cloud

        Returns:
            str: The name under which the file was uploaded
            * The name assigned after uploading to the cloud may be different from the
            original name because it is already taken in the cloud.
        """
        pass

    def get_all_files(
        self,
        remote_path: Path,
    ) -> list:
        """Get a list of files in the cloud. File objects or just file names,
          but not their actual contents.

        Args:
            remote_path (Path): The path to the folder from which you want to retrieve
            the files.
            *

        Returns:
            list: By default, all files in the default folder will be returned.
        """
        pass

    def remove_file(
        self,
        filename: str,
        remote_path: Path,
    ) -> None:
        """Delete a file in the cloud by his cfl

        Args:
            filename (str): File name in the cloud
            remote_path (Path): Path to the file in the cloud
        """
        pass

    def info(self, path: Path) -> dict:
        """Print information about the file

        Args:
            path (Path): Path to a file in the cloud

        Returns:
            dict: Information that will be displayed to the user
        """
        pass
