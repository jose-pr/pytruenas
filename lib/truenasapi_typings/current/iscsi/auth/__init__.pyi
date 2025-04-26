from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class IscsiAuth(_NS):
    
    def create(self,
        data:data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiAuthCreate:
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
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiAuthGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[IscsiAuthQueryResultItem]|IscsiAuthQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        data:data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiAuthUpdate:
        """Update iSCSI Authorized Access of `id`."""
        ...
data = _ty.TypedDict('data', {
    'tag': _ty.NotRequired[int],
    'user': _ty.NotRequired[str],
    'secret': _ty.NotRequired[str],
    'peeruser': _ty.NotRequired[str],
    'peersecret': _ty.NotRequired[str],
    'discovery_auth': _ty.NotRequired[str], 
})
IscsiAuthCreate = _ty.TypedDict('IscsiAuthCreate', {
    'id': int,
    'tag': int,
    'user': str,
    'secret': str,
    'peeruser': _ty.NotRequired[str],
    'peersecret': _ty.NotRequired[str],
    'discovery_auth': _ty.NotRequired[str], 
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
IscsiAuthGet_instance = _ty.TypedDict('IscsiAuthGet_instance', {
    'id': int,
    'tag': int,
    'user': str,
    'secret': str,
    'peeruser': _ty.NotRequired[str],
    'peersecret': _ty.NotRequired[str],
    'discovery_auth': _ty.NotRequired[str], 
})
IscsiAuthQueryResultItem = _ty.TypedDict('IscsiAuthQueryResultItem', {
    'id': _ty.NotRequired[int],
    'tag': _ty.NotRequired[int],
    'user': _ty.NotRequired[str],
    'secret': _ty.NotRequired[str],
    'peeruser': _ty.NotRequired[str],
    'peersecret': _ty.NotRequired[str],
    'discovery_auth': _ty.NotRequired[str], 
})
IscsiAuthUpdate = _ty.TypedDict('IscsiAuthUpdate', {
    'id': int,
    'tag': int,
    'user': str,
    'secret': str,
    'peeruser': _ty.NotRequired[str],
    'peersecret': _ty.NotRequired[str],
    'discovery_auth': _ty.NotRequired[str], 
})