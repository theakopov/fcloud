<div align="center">
  <h1>
    <a>Fcloud</a>
  </h1>
  Fcloud is a simple utility that makes it easy to work with the cloud

<img src=https://img.shields.io/badge/cli-app-blue> <img src=https://img.shields.io/badge/version-0.9.5-orange> <img src=https://img.shields.io/badge/simple-docs-green> <img src=https://img.shields.io/badge/language-python-yellow>

<img src="https://fcloud.tech/files/how_it_works.gif" alt="Fcloud in action" width="100%">
</div>

---

<h2>Why?</h2>
In the classic sense, cloud storage works on a <i>file-to-cloud</i> basis. They represent a separate system where your files are stored. </br></br><b>Fcloud</b> offers a new approach. Fcloud integrates into the system and becomes one with your file system. When working with files, <b><i>the file structure and file names are preserved</b></i>.

<h2>Installation</h2>
<h3>Windows:</h3>
Download the ready installers here:  https://github.com/theakopov/fcloud/releases.


<h3>Linux:</h3>
Download the project using <i>pipx</i>:

```bash
pipx install https://github.com/theakopov/fcloud/archive/refs/heads/main.zip
```

> First, it must be installed on your system - [install pipx](https://pipx.pypa.io/stable/installation/)

<h2>Usage</h2>
A simple example of uploading and downloading a cloud file:

```bash
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


<h2>License</h2>

GNU General Public License version 2 ([more](https://opensource.org/license/gpl-2-0))