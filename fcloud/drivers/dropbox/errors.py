from textwrap import dedent

from ...exceptions.driver_errors import DriverError
from ...exceptions.exceptions import DriverException


class DropboxError(DriverError):
    auth_error = (
        "Auth error",
        dedent(
            """\
        Maybe the connection data is specified incorrectly
        or is missing from the configuration file. It is also 
        possible that the token has expired.
        More: http://fcloud.tech/docs/clouds/dropbox/connect/""",
        ),
    )

    perrmission_denied_error = (
        "Permission denied",
        dedent("""\
        Perhaps you have not granted permissions to the file.
        More: http://fcloud.tech/docs/clouds/dropbox/errors/"""),
    )

    invalid_token_error = (
        "Invalid token",
        """The token has expired or the token doesn't exist.""",
    )

    max_retries_error = (
        "Request limit exceeded",
        """Request limit exceeded. Try again later.""",
    )

    validation_error = (
        "Validation error",
        dedent("""\
        The data entered does not fit the template: '(/(.|[\r\n])*)?|id:.*|(ns:[0-9]+(/.*)?).
        Here is an example of a folder path: /films/2024"""),
    )

    uncorrect_data_error = (
        "Api data validation error",
        dedent("""\
        You may not have filled in the required fields in .conf or you may have entered invalid values.
        Details: {}"""),
    )

    badinput_error = (
        "BadInput Error",
        """Some of the data did not pass the api check. More details: {}""",
    )


class DropboxException(DriverException):
    pass
