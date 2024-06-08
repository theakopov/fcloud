import tempfile
import os
from textwrap import dedent
from pathlib import Path

from fcloud.utils.cfl import create_cfl, delete_cfl
from fcloud.utils.error import echo_error
from fcloud.utils.other import generate_new_name
from fcloud.utils.config import get_config_data, edit_config

TMP_DIR = tempfile.gettempdir() + os.sep
TMP_PATH = TMP_DIR + ".tmp"


def create_temp_config():
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

    with open(TMP_PATH, "w") as conf:
        conf.write(config)


def test_cfl_util():
    os.mknod(TMP_PATH)
    create_cfl(TMP_PATH, "filename", Path("/main/folder"), ex := ".ex", False)

    assert os.path.isfile(TMP_PATH + ex)
    with open(TMP_PATH + ex, "r") as cfl:
        assert cfl.read() == "%cfl:/main/folder/filename"

    delete_cfl(TMP_PATH + ex)
    assert not os.path.isfile(TMP_PATH + ex)


def test_cfl_util_near():
    os.mknod(TMP_PATH)
    create_cfl(TMP_PATH, "filename", Path("/main/folder"), ex := ".ex", True)

    assert os.path.isfile(TMP_PATH + ex)
    assert os.path.isfile(TMP_PATH)

    delete_cfl(TMP_PATH + ex)
    os.remove(TMP_PATH)


def test_echo_error():
    work_correct = False
    try:
        echo_error(("", ""), need_to_quit=True)
    except SystemExit:
        work_correct = True

    assert work_correct


def test_generate_new_name():
    result = generate_new_name(["file", "file (1)"], "file")
    assert result == "file (2)"

    result = generate_new_name(["t"], "t")
    assert result == "t (1)"


def test_config_utils():
    create_temp_config()
    os.environ["FCLOUD_CONFIG_PATH"] = TMP_PATH

    service = get_config_data("FCLOUD", "service")
    assert service == "test-service"

    edit_config("FCLOUD", "service", "dropbox")
    service = get_config_data("FCLOUD", "service")
    assert service == "dropbox"

    flag = False
    try:
        get_config_data("SOME_SERVICE", "some_parametr")
    except SystemExit:
        flag = True
    assert flag

    os.remove(TMP_PATH)
