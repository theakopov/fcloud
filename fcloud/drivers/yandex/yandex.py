from pathlib import Path

from ..base import CloudProtocol


class YandexCloud(CloudProtocol):
    def __init__(self, auth, main_folder: Path):
        pass

    def download_file(self, path: Path, local_path: Path) -> None:
        pass

    def upload_file(self, local_path: Path, path: Path) -> str:
        pass

    def get_all_files(self, remote_path: Path) -> list:
        pass

    def remove_file(self, path: Path) -> None:
        pass

    def info(self, path: Path) -> dict:
        pass
