import sys
from typing import NoReturn
from typing import Optional
from typing import TextIO


def echo_error(
    error_data: tuple[str, str],
    need_to_quit: bool = True,
    stderr: Optional[TextIO] = sys.stderr,
) -> NoReturn | None:
    """Function to call an error in the console

    Args:
        error_data (tuple[str, str]): error title and message
        need_to_quit (bool, optional): Terminates the programme
          after an error occurs. Default value is True.
    """
    title, message = error_data

    print(
        f"\r\nError: {title}\r\n{message}",
        file=stderr,
    )

    if need_to_quit:
        sys.exit(1)
