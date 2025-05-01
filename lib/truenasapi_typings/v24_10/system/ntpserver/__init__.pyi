from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Ntpserver(_NS):
    
    def _create(self,
        **fields:_ty.Unpack[NtpServerCreate],
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
        **fields:_ty.Unpack[NtpServerUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def _upsert(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[NtpServerUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def create(self,
        ntp_server_create:CreateNtpServerCreate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateReturn:
        """Add an NTP Server.

`address` specifies the hostname/IP address of the NTP server.

`burst` when enabled makes sure that if server is reachable, sends a burst of eight packets instead of one. This is designed to improve timekeeping quality with the server command.

`iburst` when enabled speeds up the initial synchronization, taking seconds rather than minutes.

`prefer` marks the specified server as preferred. When all other things are equal, this host is chosen for synchronization acquisition with the server command. It is recommended that they be used for servers with time monitoring hardware.

`minpoll` is minimum polling time in seconds. It must be a power of 2 and less than `maxpoll`.

`maxpoll` is maximum polling time in seconds. It must be a power of 2 and greater than `minpoll`.

`force` when enabled forces the addition of NTP server even if it is currently unreachable."""
        ...
    def delete(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete NTP server of `id`."""
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
    ) -> list[QueryNTPServerQueryResultItem]|QueryNTPServerQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        ntp_server_update:UpdateNtpServerUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update NTP server of `id`."""
        ...
NtpServerCreate = _ty.TypedDict('NtpServerCreate', {
    'address': str,
    'burst': _ty.NotRequired[bool],
    'iburst': _ty.NotRequired[bool],
    'prefer': _ty.NotRequired[bool],
    'minpoll': _ty.NotRequired[int],
    'maxpoll': _ty.NotRequired[int],
    'force': _ty.NotRequired[bool], 
})
Get = _ty.TypedDict('Get', {
    'id': _ty.NotRequired[int],
    'address': _ty.NotRequired[str],
    'burst': _ty.NotRequired[bool],
    'iburst': _ty.NotRequired[bool],
    'prefer': _ty.NotRequired[bool],
    'minpoll': _ty.NotRequired[int],
    'maxpoll': _ty.NotRequired[int], 
})
NtpServerUpdate = _ty.TypedDict('NtpServerUpdate', {
    'address': _ty.NotRequired[str],
    'burst': _ty.NotRequired[bool],
    'iburst': _ty.NotRequired[bool],
    'prefer': _ty.NotRequired[bool],
    'minpoll': _ty.NotRequired[int],
    'maxpoll': _ty.NotRequired[int],
    'force': _ty.NotRequired[bool], 
})
CreateNtpServerCreate = _ty.TypedDict('CreateNtpServerCreate', {
    'address': str,
    'burst': _ty.NotRequired[bool],
    'iburst': _ty.NotRequired[bool],
    'prefer': _ty.NotRequired[bool],
    'minpoll': _ty.NotRequired[int],
    'maxpoll': _ty.NotRequired[int],
    'force': _ty.NotRequired[bool], 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'id': int,
    'address': str,
    'burst': _ty.NotRequired[bool],
    'iburst': _ty.NotRequired[bool],
    'prefer': _ty.NotRequired[bool],
    'minpoll': _ty.NotRequired[int],
    'maxpoll': _ty.NotRequired[int], 
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
    'address': str,
    'burst': _ty.NotRequired[bool],
    'iburst': _ty.NotRequired[bool],
    'prefer': _ty.NotRequired[bool],
    'minpoll': _ty.NotRequired[int],
    'maxpoll': _ty.NotRequired[int], 
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
QueryNTPServerQueryResultItem = _ty.TypedDict('QueryNTPServerQueryResultItem', {
    'id': _ty.NotRequired[int],
    'address': _ty.NotRequired[str],
    'burst': _ty.NotRequired[bool],
    'iburst': _ty.NotRequired[bool],
    'prefer': _ty.NotRequired[bool],
    'minpoll': _ty.NotRequired[int],
    'maxpoll': _ty.NotRequired[int], 
})
UpdateNtpServerUpdate = _ty.TypedDict('UpdateNtpServerUpdate', {
    'address': _ty.NotRequired[str],
    'burst': _ty.NotRequired[bool],
    'iburst': _ty.NotRequired[bool],
    'prefer': _ty.NotRequired[bool],
    'minpoll': _ty.NotRequired[int],
    'maxpoll': _ty.NotRequired[int],
    'force': _ty.NotRequired[bool], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'address': str,
    'burst': _ty.NotRequired[bool],
    'iburst': _ty.NotRequired[bool],
    'prefer': _ty.NotRequired[bool],
    'minpoll': _ty.NotRequired[int],
    'maxpoll': _ty.NotRequired[int], 
})