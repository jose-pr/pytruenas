from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class IscsiTargetextent(_NS):
    
    def create(self,
        iscsi_target_to_extent_create:iscsi_target_to_extent_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiTargetextentCreate:
        """Create an Associated Target.

`lunid` will be automatically assigned if it is not provided based on the `target`."""
        ...
    def delete(self,
        id:int,
        force:bool=False,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete Associated Target of `id`."""
        ...
    def get_instance(self,
        id:int,
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiTargetextentGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[IscsiTargetToExtentQueryResultItem]|IscsiTargetToExtentQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        iscsi_target_to_extent_update:iscsi_target_to_extent_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiTargetextentUpdate:
        """Update Associated Target of `id`."""
        ...
iscsi_target_to_extent_create = _ty.TypedDict('iscsi_target_to_extent_create', {
    'target': int,
    'lunid': _ty.NotRequired[int|None],
    'extent': int, 
})
IscsiTargetextentCreate = _ty.TypedDict('IscsiTargetextentCreate', {
    'id': int,
    'target': int,
    'lunid': int,
    'extent': int, 
})
options = _ty.TypedDict('options', {
    'relationships': _ty.NotRequired[bool],
    'extend': _ty.NotRequired[str|None],
    'extend_context': _ty.NotRequired[str|None],
    'prefix': _ty.NotRequired[str|None],
    'extra': _ty.NotRequired[_jsonschema.JsonObject],
    'order_by': _ty.NotRequired[list[str]],
    'select': _ty.NotRequired[list[str|_jsonschema.JsonArray]],
    'count': _ty.NotRequired[bool],
    'get': _ty.NotRequired[bool],
    'offset': _ty.NotRequired[int],
    'limit': _ty.NotRequired[int],
    'force_sql_filters': _ty.NotRequired[bool], 
})
IscsiTargetextentGet_instance = _ty.TypedDict('IscsiTargetextentGet_instance', {
    'id': int,
    'target': int,
    'lunid': int,
    'extent': int, 
})
IscsiTargetToExtentQueryResultItem = _ty.TypedDict('IscsiTargetToExtentQueryResultItem', {
    'id': _ty.NotRequired[int],
    'target': _ty.NotRequired[int],
    'lunid': _ty.NotRequired[int],
    'extent': _ty.NotRequired[int], 
})
iscsi_target_to_extent_update = _ty.TypedDict('iscsi_target_to_extent_update', {
    'id': _ty.NotRequired[int],
    'target': _ty.NotRequired[int],
    'lunid': _ty.NotRequired[int],
    'extent': _ty.NotRequired[int], 
})
IscsiTargetextentUpdate = _ty.TypedDict('IscsiTargetextentUpdate', {
    'id': int,
    'target': int,
    'lunid': int,
    'extent': int, 
})