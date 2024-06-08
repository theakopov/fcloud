## Dropbox driver errors
Here are some common errors that can occur when working with the Dropbox driver:

### Perrmission denied
**Message:**
```
Error: Uknown error
 
Details: Error in call to API function "files/<operations>": Your app is not permitted to access this endpoint because it does not have the required scope 'files.content.read'. The owner of the app can enable the scope for the app using the Permissions tab on the App Console.
```

This is because at the time of token creation (`fcloud config dropbox get-token`), fcloud does not have access rights for the requested operation.
You need to recreate the token by first granting the necessary permissions to the application. In particular: 

* files.metadata.read
* files.content.write
* files.content.read

Access rights are regulated on the page: [https://www.dropbox.com/developers/apps/info/<your App Key>#settings](https://www.dropbox.com/developers/apps/info/<your App Key>#settings).<br>
After, use: `fcloud config dropbox get-token`


### Did not match pattern
**Message:**
```
Error: Uknown error
 
Details: did not match pattern '(/(.|[\r\n])*)?|id:.*|(ns:[0-9]+(/.*)?)'
```

The error occurs because file or folder name restrictions were violated when working with dropbox. For example, using backslash "\" instead of "/", omission of "/" in the configuration file before specifying the path to a folder in the cloud, etc.
The cause of an error can be either an incorrect entry in the configuration file or the data passed in the function arguments.

!!! note

    You should probably check the value of *main_folder* in your configuration file. It should look like this:
    */path/to/folder*


