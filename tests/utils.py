import os
import sys
import shutil
import subprocess

from functools import wraps
from contextlib import suppress
from textwrap import dedent

OUTPUT_SETTINGS = {
    "stdout": sys.stdout,
    "stderr": sys.stderr,
}


def run_command(
    *args,
    timeout: int,
    output_settings: dict = OUTPUT_SETTINGS,
) -> subprocess.CompletedProcess:
    process = subprocess.run(*args, **output_settings, timeout=timeout)
    return process


class Utils:
    def __init__(
        self,
        tmp_dir: str,
        tmp_path: str,
        keyword: str = "fcloud",
        cfl_ex: str = ".cfl",
        timeout: int = 10,
    ) -> None:
        self.KEYWORD = keyword
        self.CFL_EX = cfl_ex
        self.TIMEOUT = timeout
        self.TMP_DIR = tmp_dir
        self.TMP_PATH = tmp_path

    def catch(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            finally:
                with suppress(FileNotFoundError):
                    if os.path.isfile(self.TMP_PATH):
                        os.remove(self.TMP_PATH)
                    elif os.path.isfile(self.TMP_PATH + self.CFL_EX):
                        remove = run_command(
                            [self.KEYWORD, "remove", self.TMP_PATH + self.CFL_EX],
                            timeout=self.TIMEOUT,
                        )
                        if remove.returncode:
                            os.remove(self.TMP_PATH + self.CFL_EX)
                    elif os.path.isdir(self.TMP_DIR + "lessons"):
                        remove = run_command(
                            [self.KEYWORD, "remove", self.TMP_DIR + "lessons"],
                            timeout=self.TIMEOUT,
                        )
                        if remove.returncode:
                            shutil.rmtree(self.TMP_DIR + "lessons")

        return inner

    def add_temp_file(self, *args) -> None:
        """Adds an empty file to the cloud, cfl will be (TMP_PATH + CFL_EX)"""
        if not os.path.isfile(self.TMP_PATH):
            os.mknod(self.TMP_PATH)
        add = run_command(
            [self.KEYWORD, "add", self.TMP_PATH, *args], timeout=self.TIMEOUT
        )
        assert not add.returncode

    def remove_temp_file(self, *args) -> None:
        remove = run_command(
            [self.KEYWORD, "remove", self.TMP_PATH + self.CFL_EX, *args],
            timeout=self.TIMEOUT,
        )
        assert not remove.returncode

    def clear(self):
        files = run_command([self.KEYWORD, "files"], timeout=self.TIMEOUT)
        assert not files.returncode

    def create_temp_dir(self) -> str:
        folders = [
            main_folder := f"{self.TMP_DIR}lessons{os.sep}",
            f"{main_folder}russian",
            f"{main_folder}russian{os.sep}grammar",
        ]
        for folder in folders:
            os.makedirs(folder)

        files = [
            f"{main_folder}homework.txt",
            f"{main_folder}russian{os.sep}my_plane.docx",
            f"{main_folder}russian{os.sep}grammar{os.sep}lesson.mp4",
        ]
        for file in files:
            os.mknod(file)

        return main_folder

    def create_temp_config(self):
        config = dedent("""\
                [FCLOUD]
                service = test-service
                main_folder = /test/folder
                cfl_extension = .cfl

                [DROPBOX]
                token =  
                app_secret =  
                app_key = 
                """)

        with open(self.TMP_PATH, "w") as conf:
            conf.write(config)
