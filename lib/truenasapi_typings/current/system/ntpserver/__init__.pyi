from pytruenas import Namespace as _NS
import typing as _ty 
class SystemNtpserver(_NS):
    
    def create(self,
        ntp_server_create,
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
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SystemNtpserverDelete:
        """Delete NTP server of `id`."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SystemNtpserverGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SystemNtpserverQuery:
        """"""
        ...
    def update(self,
        id,
        ntp_server_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SystemNtpserverUpdate:
        """Update NTP server of `id`."""
        ...
class SystemNtpserverCreate(_ty.TypedDict):
    ...
class SystemNtpserverDelete(_ty.TypedDict):
    ...
class SystemNtpserverGet_instance(_ty.TypedDict):
    ...
class SystemNtpserverQuery(_ty.TypedDict):
    ...
class SystemNtpserverUpdate(_ty.TypedDict):
    ... 