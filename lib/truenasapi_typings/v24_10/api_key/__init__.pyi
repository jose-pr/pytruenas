from pytruenas import Namespace as _NS
import typing as _ty 
class Api_key(_NS):
    
    def create(self,
        api_key_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Api_keyCreate:
        """Creates API Key.

`name` is a user-readable name for key."""
        ...
    def delete(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Api_keyDelete:
        """Delete API Key `id`."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Api_keyGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def my_keys(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Api_keyMy_keys:
        """Get the existing API keys for the currently-authenticated user"""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Api_keyQuery:
        """"""
        ...
    def update(self,
        id,
        api_key_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Api_keyUpdate:
        """Update API Key `id`.

Specify `reset: true` to reset this API Key."""
        ...
class Api_keyCreate(_ty.TypedDict):
    ...
class Api_keyDelete(_ty.TypedDict):
    ...
class Api_keyGet_instance(_ty.TypedDict):
    ...
class Api_keyMy_keys(_ty.TypedDict):
    ...
class Api_keyQuery(_ty.TypedDict):
    ...
class Api_keyUpdate(_ty.TypedDict):
    ... 