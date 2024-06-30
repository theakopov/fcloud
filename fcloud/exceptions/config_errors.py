from textwrap import dedent

from .file_errors import FileError


class ConfigError(FileError):
    service_error = (
        "Config error",
        "Can`t parse 'service' from '.conf'. Look at '.conf.example'",
    )

    main_folder_error = (
        "Main folder error",
        "Cant`t parse 'main_folder' from '.conf'. Look at '.conf.example'",
    )

    cfl_extension_error = (
        "CFL extension error",
        "Cant`t parse 'cfl_extension' from '.conf'. Look at '.conf.example'",
    )

    section_error = (
        "Section error",
        "Can`t find required section",
    )

    config_not_found = (
        "Can`t find config file",
        ".conf need to be in <programm folder>/fcloud",
    )

    field_emty_error = (
        "The required '{}' field is missing",
        dedent("""\
        The field required by fcloud is empty.  Use 'fcloud config set-parametr {} {} <value>' to set the required value. 
        * Substitute the required value in place of <value>.
        """),
    )
