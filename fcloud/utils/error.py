import sys
from functools import wraps

from ..exceptions.exceptions import FcloudException


def catch_error(func):
    """Catch and print FcloudException errors"""

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FcloudException as err:
            print(
                f"\rError: {err.title}\r\n{err.message}",
                file=sys.stderr,
            )

            sys.exit(1)

    return inner
