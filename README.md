# Fcloud

<img src=https://img.shields.io/badge/cli-app-blue> <img src=https://img.shields.io/badge/version-0.9.0-orange> <img src=https://img.shields.io/badge/simple-docs-green> <img src=https://img.shields.io/badge/language-python-yellow>

<img src="https://fcloud.tech/files/work_example.gif" alt="Fcloud in action" width="100%"/>


**Fcloud is a simple utility that makes it easy to work with the cloud**
---

## Why?
In the classic sense, cloud storage works on a *file-to-cloud* basis. They represent a separate system where your files are stored. </br></br>*Fcloud* offers a new approach. Fcloud integrates into the system and becomes one with your file system. When working with files, **the file structure and file names are preserved**.

## Installation
#### Windows:
Download the ready installers here:  https://github.com/theakopov/fcloud/releases.


#### Linux:
Download the project using *pipx*:
```bash
pipx install git+https://github.com/theakopov/fcloud
```

> First, it must be installed on your system - [https://pipx.pypa.io/stable/installation/](https://pipx.pypa.io/stable/installation/)

## Usage
A simple example of uploading and downloading a cloud file:
```
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
```

Read more here: https://fcloud.tech/docs/usage/base/


## License

GNU General Public License version 2 ([more](https://opensource.org/license/gpl-2-0))