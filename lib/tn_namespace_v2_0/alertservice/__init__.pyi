
from pytruenas import Namespace, TrueNASClient
import typing
class Alertservice(Namespace):
    _namespace:typing.Literal['alertservice']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        alert_service_create:'AlertServiceCreate'={},
    /) -> 'AlertserviceCreateReturns': 
        """
        Create an Alert Service of specified `type`.
        
        If `enabled`, it sends alerts to the configured `type` of Alert Service.

        Parameters
        ----------
        alert_service_create:
            alert_service_create
        Returns
        -------
        AlertserviceCreateReturns:
            alertservice_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete Alert Service of `id`.

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
    def list_types(self, 
    /) -> 'list[AlertServiceType]': 
        """
        List all types of supported Alert services which can be configured with the system.

        Parameters
        ----------
        Returns
        -------
        list[AlertServiceType]:
            alert_service_types
        """
        ...
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'list[AlertserviceEntry]|AlertserviceEntry|int|AlertserviceEntry': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list[AlertserviceEntry]:
            
        AlertserviceEntry:
            
        int:
            
        AlertserviceEntry:
            
        """
        ...
    @typing.overload
    def test(self, 
        alert_service_create:'AlertServiceCreate_'={},
    /) -> 'bool': 
        """
        Send a test alert using `type` of Alert Service.

        Parameters
        ----------
        alert_service_create:
            alert_service_create
        Returns
        -------
        bool:
            Is `true` if test is successful
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        alert_service_update:'AlertServiceUpdate'={},
    /) -> 'AlertserviceUpdateReturns': 
        """
        Update Alert Service of `id`.

        Parameters
        ----------
        id:
            Update Alert Service of `id`.
        alert_service_update:
            alert_service_update
        Returns
        -------
        AlertserviceUpdateReturns:
            alertservice_update_returns
        """
        ...

class AlertServiceCreate(typing.TypedDict):
        name:'str'
        type:'str'
        attributes:'dict[str]'
        level:'str'
        enabled:'bool'
        ...
class AlertserviceCreateReturns(typing.TypedDict):
        name:'str'
        type:'str'
        attributes:'dict[str]'
        level:'str'
        enabled:'bool'
        id:'int'
        type__title:'str'
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
class AlertServiceType(typing.TypedDict):
        name:'str'
        title:'str'
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
class AlertserviceEntry(typing.TypedDict):
        name:'str'
        type:'str'
        attributes:'dict[str]'
        level:'str'
        enabled:'bool'
        id:'int'
        type__title:'str'
        ...
class AlertServiceCreate_(typing.TypedDict):
        name:'str'
        type:'str'
        attributes:'dict[str]'
        level:'str'
        enabled:'bool'
        ...
class AlertServiceUpdate(typing.TypedDict):
        name:'str'
        type:'str'
        attributes:'dict[str]'
        level:'str'
        enabled:'bool'
        ...
class AlertserviceUpdateReturns(typing.TypedDict):
        name:'str'
        type:'str'
        attributes:'dict[str]'
        level:'str'
        enabled:'bool'
        id:'int'
        type__title:'str'
        ...
