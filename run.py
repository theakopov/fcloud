"""
A simple example of usage:
$ ls
> film.mp4 # 2 gb

$ fcloud add film.mp4 --near
$ ls
> film.mp4 # 2 gb
  film.mp4.cfl # 10 bytes

$ fcloud info film.mp4.cfl
> Path:         /films/film.mp4
  Modified:     2024-02-28 12:10:30
  Size:         2147483648B
  Content_hash: 27a4179db8648f2a0358844a34c7e0a42d8fb3fbdce006b1002c7401fee581b0

$ rm film.mp4
$ ls
> film.mp4.cfl # 10 bytes

$ fcloud get film.mp4.cfl
$ ls
> film.mp4  # 2 gb

Read more - https://fcloud.tech/docs/usage/commands/
"""

import contextlib
from fcloud.main import main

if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        main()
