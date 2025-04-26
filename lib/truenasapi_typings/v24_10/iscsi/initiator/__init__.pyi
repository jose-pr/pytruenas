from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class IscsiInitiator(_NS):
    
    def create(self,
        iscsi_initiator_create:iscsi_initiator_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiInitiatorCreate:
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
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiInitiatorGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[IscsiInitiatorQueryResultItem]|IscsiInitiatorQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        iscsi_initiator_update:iscsi_initiator_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiInitiatorUpdate:
        """Update iSCSI initiator of `id`."""
        ...
iscsi_initiator_create = _ty.TypedDict('iscsi_initiator_create', {
    'initiators': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str], 
})
IscsiInitiatorCreate = _ty.TypedDict('IscsiInitiatorCreate', {
    'id': int,
    'initiators': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str], 
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
IscsiInitiatorGet_instance = _ty.TypedDict('IscsiInitiatorGet_instance', {
    'id': int,
    'initiators': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str], 
})
IscsiInitiatorQueryResultItem = _ty.TypedDict('IscsiInitiatorQueryResultItem', {
    'id': _ty.NotRequired[int],
    'initiators': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str], 
})
iscsi_initiator_update = _ty.TypedDict('iscsi_initiator_update', {
    'id': _ty.NotRequired[int],
    'initiators': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str], 
})
IscsiInitiatorUpdate = _ty.TypedDict('IscsiInitiatorUpdate', {
    'id': int,
    'initiators': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str], 
})