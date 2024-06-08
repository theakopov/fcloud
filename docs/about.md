# Fcloud

**Fcloud** is an open source Python console utility designed to interact with cloud storage directly from your system.
Fcloud allows you to preserve the file structure when working with files.

The core element of fcloud's operation is the *cfl* - *Cloud File Link*. This is a file that links to a
file in your cloud. It is used to work with cloud storage. 

When sending a file to the cloud, by default it is replaced by cfl and its weight is approximately 20 bytes. When uploading it will be replaced by the original file.
# Why Fcloud?
Fcloud is easy to use and works independently of any specific cloud storage provider. We strive to make Fcloud as user-friendly as possible.