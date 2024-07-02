from typing import Protocol
from typing import Optional
from pathlib import Path


class CloudProtocol(Protocol):
    def __init__(self, auth, main_folder: Path):
        pass

    def download_file(
        self,
        name: str,
        local_path: Path,
        remote_path: Optional[Path] = None,
    ) -> None:
        pass

    def upload_file(
        self,
        local_path: Path,
        filename: Optional[str] = None,
        remote_path: Optional[Path] = None,
    ) -> str:
        pass

    def get_all_files(
        self,
        remote_path: Optional[Path] = None,
    ) -> list:
        pass

    def remove_file(
        self,
        filename: str,
        remote_path: Optional[Path] = None,
    ) -> None:
        pass

    def info(self, cfl: Path) -> dict:
        pass
