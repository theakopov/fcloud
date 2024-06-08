# Configuration fcloud

!!! important

    Fcloud uses a `.conf` configuration file in the `.ini` format. During its operation, Fcloud relies on the FCLOUD_CONFIG_PATH environment variable. If this variable is not initialized at startup, Fcloud will attempt to use the .conf file from the source code directory where Fcloud was installed. By default, this configuration file is already present and does not need to be manually installed.

You can work with the configuration file in two methods:

1. You can get information about where it is located by using `fcloud config path`.

2. Using high-level functions in the `fcloud config` command group

#### Working with a configuration file
In the first method, understanding the structure of the Fcloud configuration file is essential. The structure is quite simple:
```ini
[FCLOUD] # General fcloud settings
service = dropbox # The service whose driver you need to use
main_folder = # The folder, in cloud storage, where you want fcloud to save all your files to
cfl_extension = .cfl # The extension that will be assigned to the file after it is uploaded to the cloud

# Below are the private settings for drivers

[DROPBOX] 
token = 
app_secret = 
app_key = 

...
```

#### Using high-level commands
Fcloud provides the following commands for working with configuration files:

* `set-cloud`
* `set-main-folder`
* `set-cfl-ex`
* `set-parametr`

### set-cloud 
> Specifies the name of the service in the configuration file whose driver is to be used

*Arguments:*

`-n --name` - Service name

### set-main-folder 
> Specifies the path to the folder where fcloud will save all the files you choose to upload

*Arguments:*

`-p --path` - Cloud folder path

### set-cfl-ex 
> Specifies which extension to assign to CFL files (files uploaded to the cloud)

*Arguments:*

`-e --extension` - Extension. If you don't want fcloud to change file names after uploading, leave this field blank


### set-parametr
> Specifies which extension to assign to CFL files (files uploaded to the cloud)

*Arguments:*

`-s --section` - The section in the configuration file whose parameter you want to change. For example, for general fcloud settings it is necessary to change the FCLOUD section (see above for more details on the configuration file structure)

`-p --parametr_name` - The name of the parameter to be changed. For example: service, main_folder, cfl_extension

`-v --value` - The value to be assigned to the parameter

*Usage example:*

    fcloud config set-parametr FCLOUD service dropbox
> This command modifies the FCLOUD section (fcloud general settings) by assigning the values service - dropbox