"""
Running the tests will create temporary files and send them
to the cloud by checking the fcloud commands, and delete
them if the remove function works correctly.

!!! To use the tests, please connect fcloud to some driver.

Note: Before running the tests again, please make sure that
all the temporary files have been deleted and also have been
deleted from the cloud. During the tests, a $TMP_PATH file
will be created in the $TMP_DIR directory. Also, in addition
to a separate file, a folder named ‘lessons’ will be created
during the tests.
"""

import subprocess
import os
import shutil
import tempfile

KEYWORD = "fcloud"
CFL_EX = ".cfl"
TIMEOUT = 10  # seconds
TMP_DIR = tempfile.gettempdir() + os.sep
TMP_PATH = TMP_DIR + ".tmp"

OUTPUT_SETTINGS = {
    "stdout": subprocess.PIPE,
    "stderr": subprocess.PIPE,
}


def run_command(
    *args,
    timeout: int = TIMEOUT,
    output_settings: dict = OUTPUT_SETTINGS,
) -> subprocess.CompletedProcess:
    process = subprocess.run(*args, **output_settings, timeout=timeout)
    return process


def catch(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            if os.path.isfile(TMP_PATH):
                os.remove(TMP_PATH)
            elif os.path.isfile(TMP_PATH + CFL_EX):
                remove = run_command([KEYWORD, "remove", TMP_PATH + CFL_EX])
                if remove.returncode:
                    os.remove(TMP_PATH + CFL_EX)
            elif os.path.isdir(TMP_DIR + "lessons"):
                shutil.rmtree(TMP_DIR + "lessons")
            raise

    return inner


def add_temp_file(*args) -> None:
    """Adds an empty file to the cloud, cfl will be (TMP_PATH + CFL_EX)"""
    if not os.path.isfile(TMP_PATH):
        os.mknod(TMP_PATH)
    add = run_command([KEYWORD, "add", TMP_PATH, *args])
    assert not add.returncode


def remove_temp_file(*args) -> None:
    remove = run_command([KEYWORD, "remove", TMP_PATH + CFL_EX, *args])
    assert not remove.returncode


def clear():
    files = run_command([KEYWORD, "files"])
    assert not files.returncode


def create_temp_dir() -> str:
    folders = [
        main_fodler := f"{TMP_DIR}lessons{os.sep}",
        f"{main_fodler}russian",
        f"{main_fodler}russian{os.sep}grammar",
    ]
    for folder in folders:
        os.makedirs(folder)

    files = [
        f"{main_fodler}homework.txt",
        f"{main_fodler}russian{os.sep}my_plane.docx",
        f"{main_fodler}russian{os.sep}grammar{os.sep}lesson.mp4",
    ]
    for file in files:
        os.mknod(file)

    return main_fodler


@catch
def test_add():
    add_temp_file()

    with open(TMP_PATH + CFL_EX, "r") as file:
        assert file.read().startswith("%cfl:")

    remove_temp_file()
    assert not os.path.isfile(TMP_PATH + CFL_EX)


@catch
def test_get():
    with open(TMP_PATH, "w") as file:
        file.write(t := "Some text")
    original_hash = hash(t)

    add = run_command([KEYWORD, "add", TMP_PATH])
    assert not add.returncode

    get = run_command([KEYWORD, "get", TMP_PATH + CFL_EX])
    assert not get.returncode

    with open(TMP_PATH, "r") as file:
        secondary_hash = hash(file.read())
    os.remove(TMP_PATH)

    assert original_hash == secondary_hash


@catch
def test_param_near():
    from time import sleep

    sleep(10)
    add_temp_file("--near")
    assert os.path.isfile(TMP_PATH)
    assert os.path.isfile(TMP_PATH + CFL_EX)

    get = run_command([KEYWORD, "get", TMP_PATH + CFL_EX, "--near"])
    assert not get.returncode
    assert os.path.isfile(TMP_PATH)
    assert os.path.isfile(TMP_PATH + CFL_EX)

    os.remove(TMP_PATH)
    remove_temp_file()


@catch
def test_remove_only_in_cloud():
    add_temp_file()

    remove_temp_file("--only-in-cloud")
    assert os.path.isfile(TMP_PATH + CFL_EX)
    os.remove(TMP_PATH + CFL_EX)


@catch
def test_with_dir():
    main_fodler = create_temp_dir()

    add = run_command([KEYWORD, "add", TMP_DIR + "lessons"], timeout=TIMEOUT * 2)
    assert not add.returncode
    assert os.path.isfile(f"{main_fodler}homework.txt{CFL_EX}")
    assert os.path.isfile(f"{main_fodler}russian{os.sep}my_plane.docx{CFL_EX}")
    assert os.path.isfile(
        f"{main_fodler}russian{os.sep}grammar{os.sep}lesson.mp4{CFL_EX}"
    )

    get = run_command([KEYWORD, "get", TMP_DIR + "lessons"], timeout=TIMEOUT * 2)
    assert not get.returncode
    assert not add.returncode
    assert os.path.isfile(f"{main_fodler}homework.txt")
    assert os.path.isfile(f"{main_fodler}russian{os.sep}my_plane.docx")
    assert os.path.isfile(f"{main_fodler}russian{os.sep}grammar{os.sep}lesson.mp4")

    shutil.rmtree(main_fodler)
