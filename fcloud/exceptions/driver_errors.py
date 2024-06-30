from .base_errors import FcloudError


class DriverError(FcloudError):
    """Basic error for working with API"""

    driver_error = (
        "Driver Error",
        """Can`t find any driver for '{}'. Officially supported drivers: https://fcloud.tech/docs/#cloud-storage-supported""",
    )

    connection_error = (
        "Connection error",
        "Check your internet connection or try again later",
    )
