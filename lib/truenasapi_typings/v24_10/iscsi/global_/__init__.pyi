from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class IscsiGlobal(_NS):
    
    def alua_enabled(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Returns whether iSCSI ALUA is enabled or not."""
        ...
    def client_count(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> int:
        """Return currently connected clients count."""
        ...
    def config(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiGlobalConfig:
        """"""
        ...
    def iser_enabled(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Returns whether iSER is enabled or not."""
        ...
    def sessions(self,
        query_filters:_jsonschema.JsonArray=[],
        query_options:query_options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[IscsiSessionQueryResultItem]|IscsiSessionQueryResultItem|int:
        """Get a list of currently running iSCSI sessions. This includes initiator and target names and the unique connection IDs."""
        ...
    def update(self,
        iscsi_update:iscsi_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiGlobalUpdate:
        """`alua` is a no-op for FreeNAS."""
        ...
IscsiGlobalConfig = _ty.TypedDict('IscsiGlobalConfig', {
    'id': int,
    'basename': str,
    'isns_servers': list[str],
    'listen_port': _ty.NotRequired[int],
    'pool_avail_threshold': _ty.NotRequired[int|None],
    'alua': bool,
    'iser': bool, 
})
query_options = _ty.TypedDict('query_options', {
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
IscsiSessionQueryResultItem = _ty.TypedDict('IscsiSessionQueryResultItem', {
    'initiator': _ty.NotRequired[str],
    'initiator_addr': _ty.NotRequired[str],
    'initiator_alias': _ty.NotRequired[str|None],
    'target': _ty.NotRequired[str],
    'target_alias': _ty.NotRequired[str],
    'header_digest': _ty.NotRequired[str|None],
    'data_digest': _ty.NotRequired[str|None],
    'max_data_segment_length': _ty.NotRequired[int|None],
    'max_receive_data_segment_length': _ty.NotRequired[int|None],
    'max_xmit_data_segment_length': _ty.NotRequired[int|None],
    'max_burst_length': _ty.NotRequired[int|None],
    'first_burst_length': _ty.NotRequired[int|None],
    'immediate_data': _ty.NotRequired[bool],
    'iser': _ty.NotRequired[bool],
    'offload': _ty.NotRequired[bool], 
})
iscsi_update = _ty.TypedDict('iscsi_update', {
    'basename': _ty.NotRequired[str],
    'isns_servers': _ty.NotRequired[list[str]],
    'listen_port': _ty.NotRequired[int],
    'pool_avail_threshold': _ty.NotRequired[int|None],
    'alua': _ty.NotRequired[bool],
    'iser': _ty.NotRequired[bool], 
})
IscsiGlobalUpdate = _ty.TypedDict('IscsiGlobalUpdate', {
    'id': int,
    'basename': str,
    'isns_servers': list[str],
    'listen_port': _ty.NotRequired[int],
    'pool_avail_threshold': _ty.NotRequired[int|None],
    'alua': bool,
    'iser': bool, 
})