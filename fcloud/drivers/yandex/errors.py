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
        """The requested resource was not found. This folder or file probably does not exist""",
    )

    invalid_token_error = (
        "Invalid token",
        """The token has expired or the token doesn't exist.""",
    )


class YandexException(DriverException):
    pass
