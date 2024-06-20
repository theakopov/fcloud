from ...exceptions.base_driver_error import DriverError


class DropboxError(DriverError):
    auth_error = (
        "Auth error",
        """Maybe the connection data is specified incorrectly 
        or is missing from the configuration file. It is also 
        possible that the token has expired.
        More: http://fcloud.tech/docs/clouds/dropbox/connect/""",
    )

    perrmission_denied_error = (
        "Permission denied",
        """Perhaps you have not granted permissions to the file.
        More: http://fcloud.tech/docs/clouds/dropbox/errors/""",
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
        """The data entered does not fit the template: '(/(.|[\r\n])*)?|id:.*|(ns:[0-9]+(/.*)?).
        Here is an example of a folder path: /films/2024""",
    )

    uncorrect_data_error = (
        "Api data validation error",
        """You may not have filled in the required fields in .conf or you may have entered invalid values.
        Details: {}""",
    )

    badinput_error = (
        "BadInput Error",
        """Some of the data did not pass the api check. More details: {}""",
    )
