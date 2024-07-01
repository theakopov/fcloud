import os
from textwrap import dedent

from .file_errors import FileError


class ConfigError(FileError):
    service_error = (
        "Config error",
        dedent(f"""\
        Can`t parse 'service' from '{os.environ.get('FCLOUD_CONFIG_PATH')}'. Most likely your configuration file 
        is corrupted. You can reinstall fcloud or manually replace the configuration file with 
        this one: https://github.com/theakopov/fcloud/blob/main/fcloud/.conf.'"""),
    )

    main_folder_error = (
        "Main folder error",
        dedent(f"""\
        Can`t parse 'main_folder' from '{os.environ.get('FCLOUD_CONFIG_PATH')}'. Most likely your configuration file
        is corrupted. You can reinstall fcloud or manually replace the configuration file with
        this one: https://github.com/theakopov/fcloud/blob/main/fcloud/.conf.'"""),
    )

    cfl_extension_error = (
        "CFL extension error",
        dedent(f"""\
        Can`t parse 'cfl_extension' from '{os.environ.get('FCLOUD_CONFIG_PATH')}'. Most likely your configuration file 
        is corrupted. You can reinstall fcloud or manually replace the configuration file with 
        this one: https://github.com/theakopov/fcloud/blob/main/fcloud/.conf.'"""),
    )

    section_error = (
        "Section error",
        "Can`t find required section",
    )

    config_not_found = (
        "Can`t find config file",
        ".conf need to be in <programm folder>/fcloud or be in the environment variable $FCLOUD_CONFIG_PATH",
    )

    field_emty_error = (
        "The required '{}' field is missing",
        dedent("""\
        The field required by fcloud is empty.  Use 'fcloud config set-parametr {} {} <value>' to set the required value. 
        * Substitute the required value in place of <value>.
        """),
    )
