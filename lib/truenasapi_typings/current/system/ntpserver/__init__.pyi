from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class SystemNtpserver(_NS):
    
    def create(self,
        ntp_server_create:ntp_server_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SystemNtpserverCreate:
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
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SystemNtpserverGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[NTPServerQueryResultItem]|NTPServerQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        ntp_server_update:ntp_server_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SystemNtpserverUpdate:
        """Update NTP server of `id`."""
        ...
ntp_server_create = _ty.TypedDict('ntp_server_create', {
    'address': str,
    'burst': _ty.NotRequired[bool],
    'iburst': _ty.NotRequired[bool],
    'prefer': _ty.NotRequired[bool],
    'minpoll': _ty.NotRequired[int],
    'maxpoll': _ty.NotRequired[int],
    'force': _ty.NotRequired[bool], 
})
SystemNtpserverCreate = _ty.TypedDict('SystemNtpserverCreate', {
    'id': int,
    'address': str,
    'burst': _ty.NotRequired[bool],
    'iburst': _ty.NotRequired[bool],
    'prefer': _ty.NotRequired[bool],
    'minpoll': _ty.NotRequired[int],
    'maxpoll': _ty.NotRequired[int], 
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
SystemNtpserverGet_instance = _ty.TypedDict('SystemNtpserverGet_instance', {
    'id': int,
    'address': str,
    'burst': _ty.NotRequired[bool],
    'iburst': _ty.NotRequired[bool],
    'prefer': _ty.NotRequired[bool],
    'minpoll': _ty.NotRequired[int],
    'maxpoll': _ty.NotRequired[int], 
})
NTPServerQueryResultItem = _ty.TypedDict('NTPServerQueryResultItem', {
    'id': _ty.NotRequired[int],
    'address': _ty.NotRequired[str],
    'burst': _ty.NotRequired[bool],
    'iburst': _ty.NotRequired[bool],
    'prefer': _ty.NotRequired[bool],
    'minpoll': _ty.NotRequired[int],
    'maxpoll': _ty.NotRequired[int], 
})
ntp_server_update = _ty.TypedDict('ntp_server_update', {
    'address': _ty.NotRequired[str],
    'burst': _ty.NotRequired[bool],
    'iburst': _ty.NotRequired[bool],
    'prefer': _ty.NotRequired[bool],
    'minpoll': _ty.NotRequired[int],
    'maxpoll': _ty.NotRequired[int],
    'force': _ty.NotRequired[bool], 
})
SystemNtpserverUpdate = _ty.TypedDict('SystemNtpserverUpdate', {
    'id': int,
    'address': str,
    'burst': _ty.NotRequired[bool],
    'iburst': _ty.NotRequired[bool],
    'prefer': _ty.NotRequired[bool],
    'minpoll': _ty.NotRequired[int],
    'maxpoll': _ty.NotRequired[int], 
})