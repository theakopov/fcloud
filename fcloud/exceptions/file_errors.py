from .base_errors import FcloudError


class FileError(FcloudError):
    not_exists_error = (
        "File is not exists",
        "Unable to find this file",
    )

    perrmission_denied = (
        "Permission denied",
        "Access rights error",
    )
