import animation as _animation
import cursor


import os
import functools
from sys import stdout


def animation(
    title: str = "Waiting",
    animation_symbols: list = ["|", "/", "-", "|", "-", "\\"],
    speed: float = 0.4,
):
    def decorator(
        func,
    ):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if ("without_animation", True) in kwargs.items():
                return func(*args, **kwargs)
            try:
                columns, _ = os.get_terminal_size()
            except OSError:
                columns = 10
            output = title + "  " + ((columns - len(title) - 15) * "." + "  ")
            stdout.write(output)
            cursor.hide()

            wait = _animation.Wait(animation_symbols, speed)
            wait.start()
            try:
                return func(*args, **kwargs)
            finally:
                cursor.show()
                wait.stop()

        return wrapper

    return decorator
