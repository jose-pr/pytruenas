from pytruenas import Namespace as _NS 
class SystemNtpserver(_NS):
    
    def create(self,
        ntp_server_create,
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
    ) -> SystemNtpserverDelete:
        """Delete NTP server of `id`."""
        ...
    def get_instance(self,
        id,
        options,
    ) -> SystemNtpserverGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
    ) -> SystemNtpserverQuery:
        """"""
        ...
    def update(self,
        id,
        ntp_server_update,
    ) -> SystemNtpserverUpdate:
        """Update NTP server of `id`."""
        ...
class SystemNtpserverCreate:
    ...
class SystemNtpserverDelete:
    ...
class SystemNtpserverGet_instance:
    ...
class SystemNtpserverQuery:
    ...
class SystemNtpserverUpdate:
    ... 