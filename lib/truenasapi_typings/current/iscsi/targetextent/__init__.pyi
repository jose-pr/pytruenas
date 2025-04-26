from pytruenas import Namespace as _NS
import typing as _ty 
class IscsiTargetextent(_NS):
    
    def create(self,
        iscsi_target_to_extent_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiTargetextentCreate:
        """Create an Associated Target.

`lunid` will be automatically assigned if it is not provided based on the `target`."""
        ...
    def delete(self,
        id,
        force,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiTargetextentDelete:
        """Delete Associated Target of `id`."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiTargetextentGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiTargetextentQuery:
        """"""
        ...
    def update(self,
        id,
        iscsi_target_to_extent_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiTargetextentUpdate:
        """Update Associated Target of `id`."""
        ...
class IscsiTargetextentCreate(_ty.TypedDict):
    ...
class IscsiTargetextentDelete(_ty.TypedDict):
    ...
class IscsiTargetextentGet_instance(_ty.TypedDict):
    ...
class IscsiTargetextentQuery(_ty.TypedDict):
    ...
class IscsiTargetextentUpdate(_ty.TypedDict):
    ... 