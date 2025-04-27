from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Initiator(_NS):
    
    def _create(self,
        **fields:_ty.Unpack[IscsiInitiatorCreate],
    ) -> CreateReturn:
        """"""
        ...
    def _update(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[IscsiInitiatorUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def _upsert(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[IscsiInitiatorUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def create(self,
        iscsi_initiator_create:CreateIscsiInitiatorCreate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateReturn:
        """Create an iSCSI Initiator.

`initiators` is a list of initiator hostnames which are authorized to access an iSCSI Target. To allow all possible initiators, `initiators` can be left empty."""
        ...
    def delete(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete iSCSI initiator of `id`."""
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
    ) -> list[QueryIscsiInitiatorQueryResultItem]|QueryIscsiInitiatorQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        iscsi_initiator_update:UpdateIscsiInitiatorUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update iSCSI initiator of `id`."""
        ...
IscsiInitiatorCreate = _ty.TypedDict('IscsiInitiatorCreate', {
    'initiators': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str], 
})
IscsiInitiatorUpdate = _ty.TypedDict('IscsiInitiatorUpdate', {
    'id': _ty.NotRequired[int],
    'initiators': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str], 
})
CreateIscsiInitiatorCreate = _ty.TypedDict('CreateIscsiInitiatorCreate', {
    'initiators': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str], 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'id': int,
    'initiators': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str], 
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
    'initiators': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str], 
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
QueryIscsiInitiatorQueryResultItem = _ty.TypedDict('QueryIscsiInitiatorQueryResultItem', {
    'id': _ty.NotRequired[int],
    'initiators': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str], 
})
UpdateIscsiInitiatorUpdate = _ty.TypedDict('UpdateIscsiInitiatorUpdate', {
    'id': _ty.NotRequired[int],
    'initiators': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'initiators': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str], 
})