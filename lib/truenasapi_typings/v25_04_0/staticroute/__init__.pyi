from pytruenas import Namespace as _NS
import typing as _ty 
class Staticroute(_NS):
    
    def create(self,
        data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> StaticrouteCreate:
        """Create a Static Route.

Address families of `gateway` and `destination` should match when creating a static route.

`description` is an optional attribute for any notes regarding the static route."""
        ...
    def delete(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> StaticrouteDelete:
        """Delete Static Route of `id`."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> StaticrouteGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> StaticrouteQuery:
        """"""
        ...
    def update(self,
        id,
        data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> StaticrouteUpdate:
        """Update Static Route of `id`."""
        ...
class StaticrouteCreate(_ty.TypedDict):
    ...
class StaticrouteDelete(_ty.TypedDict):
    ...
class StaticrouteGet_instance(_ty.TypedDict):
    ...
class StaticrouteQuery(_ty.TypedDict):
    ...
class StaticrouteUpdate(_ty.TypedDict):
    ... 