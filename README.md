# Description
Attempt at making Truenas Websocket Api as easy to use as possible and provide better typing support for all methods.
# TODO
* Better Codegen
    * Code/Template to decipher types for pyi files.
    * Using mako as that is already installed in Truenas but add backend for jinja or direct python files. Autodect template type.
    * Better way to resolve generics, also build TypeDict, instead of returning dict\[str\] and return list\[T\] instead of just list.
    * Possible to identify different signatures for same method, which provides what output?
* Remove Namespace tns23 and use autogen with the option to detect Config/List and use alternative query/update/config methods.