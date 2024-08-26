from textwrap import dedent

from ...exceptions.exceptions import DriverException
from ...exceptions.driver_errors import DriverError


class YandexError(DriverError):
    invalid_token_error = (
        "Invalid token",
        """The token has expired or the token doesn't exist.""",
    )

    timed_out_error = (
        "Timed out",
        """Thrown when a request timed out""",
    )

    path_not_found_error = (
        "Resource not found",
        "The requested resource (file or folder) was not found in the cloud.",
    )

    invalid_token_error = (
        "Invalid token",
        """The token has expired or the token doesn't exist.""",
    )

    access_denied = (
        "Access denied",
        dedent("""\
        Access denied. The application probably does not have sufficient 
        permissions to perform this action. You can change the application 
        settings on this page: https://oauth.yandex.ru/."""),
    )


class YandexException(DriverException):
    pass
