
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin
from enum import Enum
import typing
class Service(
    TableExtMixin,
    Namespace
    ):
    _namespace:typing.Literal['service']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def get_instance(self, 
        id:'typing.Union[str, int, bool, dict[str], list]',
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
    /) -> 'typing.Union[list[ServiceEntry], ServiceEntry_, int, ServiceEntry__]': 
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
        typing.Union[list[ServiceEntry], ServiceEntry_, int, ServiceEntry__]:
            
        """
        ...
    @typing.overload
    def reload(self, 
        service:'str',
        service_control:'ServiceControl'={},
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
    @typing.overload
    def restart(self, 
        service:'str',
        service_control:'ServiceControl'={},
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
    @typing.overload
    def start(self, 
        service:'str',
        service_control:'ServiceControl'={},
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
    @typing.overload
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
    @typing.overload
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
    @typing.overload
    def stop(self, 
        service:'str',
        service_control:'ServiceControl'={},
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
    @typing.overload
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
    @typing.overload
    def update(self, 
        id_or_name:'str',
        service_update:'ServiceUpdate'={},
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
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    ServiceEntry = typing.TypedDict('ServiceEntry', {
            'id':'int',
            'service':'str',
            'enable':'bool',
            'state':'str',
            'pids':'list[int]',
    })
    ServiceEntry_ = typing.TypedDict('ServiceEntry_', {
            'id':'int',
            'service':'str',
            'enable':'bool',
            'state':'str',
            'pids':'list[int]',
    })
    ServiceEntry__ = typing.TypedDict('ServiceEntry__', {
            'id':'int',
            'service':'str',
            'enable':'bool',
            'state':'str',
            'pids':'list[int]',
    })
    ServiceControl = typing.TypedDict('ServiceControl', {
            'ha_propagate':'bool',
            'silent':'bool',
    })
    ServiceUpdate = typing.TypedDict('ServiceUpdate', {
            'enable':'bool',
    })
