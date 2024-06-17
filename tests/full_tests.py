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

import os
import shutil
import tempfile

from .utils import Utils
from .utils import run_command

KEYWORD = "fcloud"
CFL_EX = ".cfl"
TIMEOUT = 10  # seconds
TMP_DIR = tempfile.gettempdir() + os.sep
TMP_PATH = TMP_DIR + ".tmp"

utils = Utils(TMP_DIR, TMP_PATH, KEYWORD, CFL_EX, TIMEOUT)


@utils.catch
def test_add():
    utils.create_cfl()

    with open(TMP_PATH + CFL_EX, "r") as file:
        assert file.read().startswith("%cfl:")

    utils.remove_temp_file()
    assert not os.path.isfile(TMP_PATH + CFL_EX)


@utils.catch
def test_get():
    with open(TMP_PATH, "w") as file:
        file.write(t := "Some text")
    original_hash = hash(t)

    add = run_command([KEYWORD, "add", TMP_PATH], timeout=TIMEOUT)
    assert not add.returncode

    get = run_command([KEYWORD, "get", TMP_PATH + CFL_EX], timeout=TIMEOUT)
    assert not get.returncode

    with open(TMP_PATH, "r") as file:
        secondary_hash = hash(file.read())
    os.remove(TMP_PATH)

    assert original_hash == secondary_hash


@utils.catch
def test_param_near():
    from time import sleep

    sleep(10)
    utils.create_cfl("--near")
    assert os.path.isfile(TMP_PATH)
    assert os.path.isfile(TMP_PATH + CFL_EX)

    get = run_command([KEYWORD, "get", TMP_PATH + CFL_EX, "--near"], timeout=TIMEOUT)
    assert not get.returncode
    assert os.path.isfile(TMP_PATH)
    assert os.path.isfile(TMP_PATH + CFL_EX)

    os.remove(TMP_PATH)
    utils.remove_temp_file()


@utils.catch
def test_remove_only_in_cloud():
    utils.create_cfl()

    utils.remove_temp_file("--only-in-cloud")
    assert os.path.isfile(TMP_PATH + CFL_EX)
    os.remove(TMP_PATH + CFL_EX)


@utils.catch
def test_with_dir():
    main_fodler = utils.create_temp_dir()

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
