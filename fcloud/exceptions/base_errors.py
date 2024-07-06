from textwrap import dedent


class FcloudError:
    """A class from which all classes containing error data are inherited"""

    exmaple_error = (
        "Error title",
        "Error message. Some info about error and maybe link to docs",
    )

    uknown_error = (
        "Uknown error",
        dedent("""\
        Details: {}
        Maybe, you can find more abut this error on http://fcloud.tech/docs/clouds/dropbox/errors/
        """),
    )
