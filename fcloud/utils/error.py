import sys
from functools import wraps

from ..exceptions.exceptions import FcloudException


def catch_error(debug: bool = False):
    """Catch and print FcloudException errors"""

    def decorator(func):
        """Catch and print FcloudException errors"""

        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except FcloudException as err:
                if debug:
                    raise

                print(
                    f"\rError: {err.title}\r\n{err.message}",
                    file=sys.stderr,
                )

                sys.exit(1)

        return inner

    return decorator
