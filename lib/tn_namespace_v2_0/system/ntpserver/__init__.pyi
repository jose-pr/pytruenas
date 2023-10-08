
from pytruenas import Namespace, TrueNASClient
import typing
class SystemNtpserver(Namespace):
    _namespace:typing.Literal['system.ntpserver']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        ntp_create:'NtpCreate'={},
    /) -> 'SystemNtpserverCreateReturns': 
        """
        Add an NTP Server.
        
        `address` specifies the hostname/IP address of the NTP server.
        
        `burst` when enabled makes sure that if server is reachable, sends a burst of eight packets instead of one.
        This is designed to improve timekeeping quality with the server command.
        
        `iburst` when enabled speeds up the initial synchronization, taking seconds rather than minutes.
        
        `prefer` marks the specified server as preferred. When all other things are equal, this host is chosen
        for synchronization acquisition with the server command. It is recommended that they be used for servers with
        time monitoring hardware.
        
        `minpoll` is minimum polling time in seconds. It must be a power of 2 and less than `maxpoll`.
        
        `maxpoll` is maximum polling time in seconds. It must be a power of 2 and greater than `minpoll`.
        
        `force` when enabled forces the addition of NTP server even if it is currently unreachable.

        Parameters
        ----------
        ntp_create:
            ntp_create
        Returns
        -------
        SystemNtpserverCreateReturns:
            system_ntpserver_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete NTP server of `id`.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
        """
        ...
    @typing.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'QueryOptionsGetInstance'={},
    /) -> None: 
        """
        Returns instance matching `id`. If `id` is not found, Validation error is raised.
        
        Please see `query` method documentation for `options`.

        Parameters
        ----------
        id:
            Returns instance matching `id`. If `id` is not found, Validation error is raised.
        query_options_get_instance:
            query-options-get_instance
        Returns
        -------
        """
        ...
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'list[NtpEntry]|NtpEntry|int|NtpEntry': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list[NtpEntry]:
            
        NtpEntry:
            
        int:
            
        NtpEntry:
            
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        ntp_update:'NtpUpdate'={},
    /) -> 'SystemNtpserverUpdateReturns': 
        """
        Update NTP server of `id`.

        Parameters
        ----------
        id:
            Update NTP server of `id`.
            Add an NTP Server.
        ntp_update:
            ntp_update
        Returns
        -------
        SystemNtpserverUpdateReturns:
            system_ntpserver_update_returns
        """
        ...

class NtpCreate(typing.TypedDict):
        address:'str'
        burst:'bool'
        iburst:'bool'
        prefer:'bool'
        minpoll:'int'
        maxpoll:'int'
        force:'bool'
        ...
class SystemNtpserverCreateReturns(typing.TypedDict):
        address:'str'
        burst:'bool'
        iburst:'bool'
        prefer:'bool'
        minpoll:'int'
        maxpoll:'int'
        id:'int'
        ...
class QueryOptionsGetInstance(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class QueryOptions(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class NtpEntry(typing.TypedDict):
        address:'str'
        burst:'bool'
        iburst:'bool'
        prefer:'bool'
        minpoll:'int'
        maxpoll:'int'
        id:'int'
        ...
class NtpUpdate(typing.TypedDict):
        address:'str'
        burst:'bool'
        iburst:'bool'
        prefer:'bool'
        minpoll:'int'
        maxpoll:'int'
        force:'bool'
        ...
class SystemNtpserverUpdateReturns(typing.TypedDict):
        address:'str'
        burst:'bool'
        iburst:'bool'
        prefer:'bool'
        minpoll:'int'
        maxpoll:'int'
        id:'int'
        ...