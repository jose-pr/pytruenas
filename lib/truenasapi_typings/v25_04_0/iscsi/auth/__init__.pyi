from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Auth(_NS):
    
    def _create(self,
        **fields:_ty.Unpack[Data],
    ) -> CreateReturn:
        """"""
        ...
    def _get(self,
        __id_or_filter:int|_ty.Sequence[str]|None=None,
        **fields:_ty.Unpack[Get],
    ) -> GetInstanceReturn|None:
        """"""
        ...
    def _update(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[Data],
    ) -> UpdateReturn:
        """"""
        ...
    def _upsert(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[Data],
    ) -> UpdateReturn:
        """"""
        ...
    def create(self,
        data:CreateData,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateReturn:
        """Create an iSCSI Authorized Access.

`tag` should be unique among all configured iSCSI Authorized Accesses.

`secret` and `peersecret` should have length between 12-16 letters inclusive.

`peeruser` and `peersecret` are provided only when configuring mutual CHAP. `peersecret` should not be similar to `secret`."""
        ...
    def delete(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete iSCSI Authorized Access of `id`."""
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
    ) -> list[QueryIscsiAuthQueryResultItem]|QueryIscsiAuthQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        data:UpdateData,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update iSCSI Authorized Access of `id`."""
        ...
Data = _ty.TypedDict('Data', {
    'tag': _ty.NotRequired[int],
    'user': _ty.NotRequired[str],
    'secret': _ty.NotRequired[str],
    'peeruser': _ty.NotRequired[str],
    'peersecret': _ty.NotRequired[str],
    'discovery_auth': _ty.NotRequired[str], 
})
Get = _ty.TypedDict('Get', {
    'id': _ty.NotRequired[int],
    'tag': _ty.NotRequired[int],
    'user': _ty.NotRequired[str],
    'secret': _ty.NotRequired[str],
    'peeruser': _ty.NotRequired[str],
    'peersecret': _ty.NotRequired[str],
    'discovery_auth': _ty.NotRequired[str], 
})
CreateData = _ty.TypedDict('CreateData', {
    'tag': int,
    'user': str,
    'secret': str,
    'peeruser': _ty.NotRequired[str],
    'peersecret': _ty.NotRequired[str],
    'discovery_auth': _ty.NotRequired[str], 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'id': int,
    'tag': int,
    'user': str,
    'secret': str,
    'peeruser': _ty.NotRequired[str],
    'peersecret': _ty.NotRequired[str],
    'discovery_auth': _ty.NotRequired[str], 
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
    'tag': int,
    'user': str,
    'secret': str,
    'peeruser': _ty.NotRequired[str],
    'peersecret': _ty.NotRequired[str],
    'discovery_auth': _ty.NotRequired[str], 
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
QueryIscsiAuthQueryResultItem = _ty.TypedDict('QueryIscsiAuthQueryResultItem', {
    'id': _ty.NotRequired[int],
    'tag': _ty.NotRequired[int],
    'user': _ty.NotRequired[str],
    'secret': _ty.NotRequired[str],
    'peeruser': _ty.NotRequired[str],
    'peersecret': _ty.NotRequired[str],
    'discovery_auth': _ty.NotRequired[str], 
})
UpdateData = _ty.TypedDict('UpdateData', {
    'tag': _ty.NotRequired[int],
    'user': _ty.NotRequired[str],
    'secret': _ty.NotRequired[str],
    'peeruser': _ty.NotRequired[str],
    'peersecret': _ty.NotRequired[str],
    'discovery_auth': _ty.NotRequired[str], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'tag': int,
    'user': str,
    'secret': str,
    'peeruser': _ty.NotRequired[str],
    'peersecret': _ty.NotRequired[str],
    'discovery_auth': _ty.NotRequired[str], 
})