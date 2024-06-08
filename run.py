import contextlib
from fcloud.main import main

if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        main()
