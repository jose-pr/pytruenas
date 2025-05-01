# Description
Attempt at making Truenas Websocket Api as easy to use as possible and provide better typing support for all methods.

Provide method to run commands doesnt matter if local or through ssh with a common interface

Provide a interface base on pathlib.Path to work with paths on the remote system with backend for local, and remote: sftp, api 

Provide some typings for methods.

Provide a cli program/script to run management/configuration actions based on the previous.
# TODO
* Better Codegen
    * Possible to identify different signatures for same method, which provides what output?
