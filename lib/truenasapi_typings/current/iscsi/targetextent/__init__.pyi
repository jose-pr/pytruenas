from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Targetextent(_NS):
    
    def _create(self,
        **fields:_ty.Unpack[IscsiTargetToExtentCreate],
    ) -> CreateReturn:
        """"""
        ...
    def _update(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[IscsiTargetToExtentUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def _upsert(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[IscsiTargetToExtentUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def create(self,
        iscsi_target_to_extent_create:CreateIscsiTargetToExtentCreate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateReturn:
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
        options:GetInstanceOptions={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GetInstanceReturn:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:QueryOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[QueryIscsiTargetToExtentQueryResultItem]|QueryIscsiTargetToExtentQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        iscsi_target_to_extent_update:UpdateIscsiTargetToExtentUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update Associated Target of `id`."""
        ...
IscsiTargetToExtentCreate = _ty.TypedDict('IscsiTargetToExtentCreate', {
    'target': int,
    'lunid': _ty.NotRequired[int|None],
    'extent': int, 
})
IscsiTargetToExtentUpdate = _ty.TypedDict('IscsiTargetToExtentUpdate', {
    'id': _ty.NotRequired[int],
    'target': _ty.NotRequired[int],
    'lunid': _ty.NotRequired[int],
    'extent': _ty.NotRequired[int], 
})
CreateIscsiTargetToExtentCreate = _ty.TypedDict('CreateIscsiTargetToExtentCreate', {
    'target': int,
    'lunid': _ty.NotRequired[int|None],
    'extent': int, 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'id': int,
    'target': int,
    'lunid': int,
    'extent': int, 
})
GetInstanceOptions = _ty.TypedDict('GetInstanceOptions', {
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
GetInstanceReturn = _ty.TypedDict('GetInstanceReturn', {
    'id': int,
    'target': int,
    'lunid': int,
    'extent': int, 
})
QueryOptions = _ty.TypedDict('QueryOptions', {
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
QueryIscsiTargetToExtentQueryResultItem = _ty.TypedDict('QueryIscsiTargetToExtentQueryResultItem', {
    'id': _ty.NotRequired[int],
    'target': _ty.NotRequired[int],
    'lunid': _ty.NotRequired[int],
    'extent': _ty.NotRequired[int], 
})
UpdateIscsiTargetToExtentUpdate = _ty.TypedDict('UpdateIscsiTargetToExtentUpdate', {
    'id': _ty.NotRequired[int],
    'target': _ty.NotRequired[int],
    'lunid': _ty.NotRequired[int],
    'extent': _ty.NotRequired[int], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'target': int,
    'lunid': int,
    'extent': int, 
})