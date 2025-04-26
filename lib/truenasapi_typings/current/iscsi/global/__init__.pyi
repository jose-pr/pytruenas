from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Global(_NS):
    
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
    ) -> ConfigReturn:
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
        query_options:SessionsQueryOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[SessionsIscsiSessionQueryResultItem]|SessionsIscsiSessionQueryResultItem|int:
        """Get a list of currently running iSCSI sessions. This includes initiator and target names and the unique connection IDs."""
        ...
    def update(self,
        iscsi_update:UpdateIscsiUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """`alua` is a no-op for FreeNAS."""
        ...
ConfigReturn = _ty.TypedDict('ConfigReturn', {
    'id': int,
    'basename': str,
    'isns_servers': list[str],
    'listen_port': _ty.NotRequired[int],
    'pool_avail_threshold': _ty.NotRequired[int|None],
    'alua': bool,
    'iser': bool, 
})
SessionsQueryOptions = _ty.TypedDict('SessionsQueryOptions', {
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
SessionsIscsiSessionQueryResultItem = _ty.TypedDict('SessionsIscsiSessionQueryResultItem', {
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
UpdateIscsiUpdate = _ty.TypedDict('UpdateIscsiUpdate', {
    'basename': _ty.NotRequired[str],
    'isns_servers': _ty.NotRequired[list[str]],
    'listen_port': _ty.NotRequired[int],
    'pool_avail_threshold': _ty.NotRequired[int|None],
    'alua': _ty.NotRequired[bool],
    'iser': _ty.NotRequired[bool], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'basename': str,
    'isns_servers': list[str],
    'listen_port': _ty.NotRequired[int],
    'pool_avail_threshold': _ty.NotRequired[int|None],
    'alua': bool,
    'iser': bool, 
})