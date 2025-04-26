from pytruenas import Namespace as _NS
import typing as _ty 
class AppRegistry(_NS):
    
    def create(self,
        app_registry_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppRegistryCreate:
        """Create an app registry entry."""
        ...
    def delete(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppRegistryDelete:
        """Delete an app registry entry."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppRegistryGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppRegistryQuery:
        """"""
        ...
    def update(self,
        id,
        data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppRegistryUpdate:
        """Update an app registry entry."""
        ...
class AppRegistryCreate(_ty.TypedDict):
    ...
class AppRegistryDelete(_ty.TypedDict):
    ...
class AppRegistryGet_instance(_ty.TypedDict):
    ...
class AppRegistryQuery(_ty.TypedDict):
    ...
class AppRegistryUpdate(_ty.TypedDict):
    ... 