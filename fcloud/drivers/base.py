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
        pass

    def upload_file(
        self,
        local_path: Path,
        filename: str,
        remote_path: Path,
    ) -> str:
        pass

    def get_all_files(
        self,
        remote_path: Path,
    ) -> list:
        pass

    def remove_file(
        self,
        filename: str,
        remote_path: Path,
    ) -> None:
        pass

    def info(self, cfl: Path) -> dict:
        pass
