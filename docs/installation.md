# Installation

#### Install fcloud
You can download the project using *pipx*:
  - `pipx install git+https://github.com/theakopov/fcloud` - install source<br>
!!! important
    Ensure pipx is installed on your system first: [pipx installation guide](https://pipx.pypa.io/stable/installation/)

#### Set up

1. You need to tell fcloud which cloud storage service you will use.
 Let's take dropbox as an example
    `fcloud config set-parametr FCLOUD service dropbox`

2. Create a folder in your cloud and specify it with the following command. By default, all files will be downloaded there.*

    `fcloud config set-parametr FCLOUD main_folder </your folder name/>`<br>
For example: `fcloud config set-parametr FCLOUD main_folder /laptop`


!!! note
    You can find more information in the *CLOUDS* section of the documentation menu about the cloud you want to use.