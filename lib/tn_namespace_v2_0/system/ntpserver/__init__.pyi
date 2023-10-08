
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class SystemNtpserver(Namespace):
    _namespace:_ty.Literal['system.ntpserver']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        ntp_create:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            system_ntpserver_create_returns
        """
        ...
    @_ty.overload
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
    @_ty.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'dict[str]'={},
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
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @_ty.overload
    def update(self, 
        id:'int',
        ntp_update:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            system_ntpserver_update_returns
        """
        ...
