import tempfile
import os
from textwrap import dedent
from pathlib import Path

from fcloud.utils.cfl import create_cfl, delete_cfl
from fcloud.utils.error import echo_error
from fcloud.utils.other import generate_new_name
from fcloud.utils.config import get_config_data, edit_config
from fcloud.cli.groups.config import Config

from .utils import Utils

TMP_DIR = tempfile.gettempdir() + os.sep
TMP_PATH = TMP_DIR + ".tmp"

utils = Utils(TMP_DIR, TMP_PATH)


@utils.catch
def test_cfl_util():
    os.mknod(TMP_PATH)
    create_cfl(TMP_PATH, "filename", Path("/main/folder"), ex := ".ex", False)

    assert os.path.isfile(TMP_PATH + ex)
    with open(TMP_PATH + ex, "r") as cfl:
        assert cfl.read() == "%cfl:/main/folder/filename"

    delete_cfl(TMP_PATH + ex)
    assert not os.path.isfile(TMP_PATH + ex)


@utils.catch
def test_cfl_util_near():
    os.mknod(TMP_PATH)
    create_cfl(TMP_PATH, "filename", Path("/main/folder"), ex := ".ex", True)

    assert os.path.isfile(TMP_PATH + ex)
    assert os.path.isfile(TMP_PATH)

    delete_cfl(TMP_PATH + ex)


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


@utils.catch
def test_config_utils():
    utils.create_temp_config()
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


@utils.catch
def test_config():
    config = Config(["some_cloud", "second_cloud"], Path(TMP_PATH))
    with open(TMP_PATH, "w") as conf:
        conf.write(
            content := dedent("""\
            [FCLOUD]
            service = some_cloud
            main_folder = /test
            cfl_extension = .cfl

            [some_cloud]
            token = 123456abcdef
                """)
        )
    assert config.read() == content

    config.set_cloud("second_cloud")
    config.set_main_folder("/films")
    config.set_cfl_ex(".fcloud")

    assert config.read() == dedent("""\
            [FCLOUD]
            service = second_cloud
            main_folder = /films
            cfl_extension = .fcloud

            [some_cloud]
            token = 123456abcdef

            """)
