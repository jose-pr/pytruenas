
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Service(Namespace):
    _namespace:_ty.Literal['service']
    def __init__(self, client:TrueNASClient) -> None: ...
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
        Query all system services with `query-filters` and `query-options`.
        
        Supports the following extra options:
        `include_state` - performance optimization to avoid getting service state.
        defaults to True.

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
    def reload(self, 
        service:'str',
        service_control:'dict[str]'={},
    /) -> 'bool': 
        """
        Reload the service specified by `service`.

        Parameters
        ----------
        service:
            service
        service_control:
            service-control
        Returns
        -------
        bool:
            service_reloaded
        """
        ...
    @_ty.overload
    def restart(self, 
        service:'str',
        service_control:'dict[str]'={},
    /) -> 'bool': 
        """
        Restart the service specified by `service`.

        Parameters
        ----------
        service:
            service
        service_control:
            service-control
        Returns
        -------
        bool:
            service_restarted
        """
        ...
    @_ty.overload
    def start(self, 
        service:'str',
        service_control:'dict[str]'={},
    /) -> 'bool': 
        """
        Start the service specified by `service`.
        
        If `silent` is `true` then in case of service startup failure, `false` will be returned. If `silent` is `false`
        then in case of service startup failure, an exception will be raised.

        Parameters
        ----------
        service:
            Start the service specified by `service`.
        service_control:
            service-control
        Returns
        -------
        bool:
            started_service
        """
        ...
    @_ty.overload
    def started(self, 
        service:'str',
    /) -> 'bool': 
        """
        Test if service specified by `service` has been started.

        Parameters
        ----------
        service:
            service
        Returns
        -------
        bool:
            Will return `true` if service is running
        """
        ...
    @_ty.overload
    def started_or_enabled(self, 
        service:'str',
    /) -> 'bool': 
        """
        Test if service specified by `service` is started or enabled to start automatically.

        Parameters
        ----------
        service:
            service
        Returns
        -------
        bool:
            Will return `true` if service is started or enabled to start automatically.
        """
        ...
    @_ty.overload
    def stop(self, 
        service:'str',
        service_control:'dict[str]'={},
    /) -> 'bool': 
        """
        Stop the service specified by `service`.

        Parameters
        ----------
        service:
            service
        service_control:
            service-control
        Returns
        -------
        bool:
            Will return `true` if service successfully stopped
        """
        ...
    @_ty.overload
    def terminate_process(self, 
        pid:'int',
        timeout:'int'=10,
    /) -> 'bool': 
        """
        Terminate process by `pid`.
        
        First send `TERM` signal, then, if was not terminated in `timeout` seconds, send `KILL` signal.

        Parameters
        ----------
        pid:
            Terminate process by `pid`.
        timeout:
            timeout
        Returns
        -------
        bool:
            `true` is process has been successfully terminated with `TERM` and `false` if we had to use `KILL`
        """
        ...
    @_ty.overload
    def update(self, 
        id_or_name:'str',
        service_update:'dict[str]'={},
    /) -> 'int': 
        """
        Update service entry of `id_or_name`.
        
        Currently it only accepts `enable` option which means whether the
        service should start on boot.

        Parameters
        ----------
        id_or_name:
            Update service entry of `id_or_name`.
        service_update:
            service-update
        Returns
        -------
        int:
            service_primary_key
        """
        ...
