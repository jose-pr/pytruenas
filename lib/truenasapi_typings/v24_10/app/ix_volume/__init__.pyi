from pytruenas import Namespace as _NS
import typing as _ty 
class AppIx_volume(_NS):
    
    def exists(self,
        name,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppIx_volumeExists:
        """Check if ix-volumes exist for `app_name`."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppIx_volumeQuery:
        """Query ix-volumes with `filters` and `options`."""
        ...
class AppIx_volumeExists(_ty.TypedDict):
    ...
class AppIx_volumeQuery(_ty.TypedDict):
    ... 