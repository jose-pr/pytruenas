from pytruenas import Namespace as _NS
import typing as _ty 
class DockerNetwork(_NS):
    
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> DockerNetworkGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> DockerNetworkQuery:
        """Query all docker networks"""
        ...
class DockerNetworkGet_instance(_ty.TypedDict):
    ...
class DockerNetworkQuery(_ty.TypedDict):
    ... 