
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Alertservice(
    Namespace
    ):
    _namespace:typing.Literal['alertservice']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        _alert_service_create:'AlertServiceCreate',
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
        _id:'int',
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
        _id:'typing.Union[str, int, bool, dict[str], list]',
        _query_options_get_instance:'QueryOptionsGetInstance',
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
        _query_filters:'list[list]',
        _query_options:'QueryOptions',
    /) -> 'typing.Union[list[AlertserviceEntry], AlertserviceEntry, int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[AlertserviceEntry], AlertserviceEntry, int]:
            
        """
        ...
    @typing.overload
    def test(self, 
        _alert_service_create:'AlertServiceCreate',
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
        _id:'int',
        _alert_service_update:'AlertServiceUpdate',
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
    AlertServiceCreate = typing.TypedDict('AlertServiceCreate', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'level':'Level',
            'enabled':'bool',
    })
    AlertServiceType = typing.TypedDict('AlertServiceType', {
            'name':'str',
            'title':'str',
    })
    AlertServiceUpdate = typing.TypedDict('AlertServiceUpdate', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'level':'Level',
            'enabled':'bool',
    })
    AlertserviceCreateReturns = typing.TypedDict('AlertserviceCreateReturns', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'level':'Level',
            'enabled':'bool',
            'id':'int',
            'type__title':'str',
    })
    AlertserviceEntry = typing.TypedDict('AlertserviceEntry', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'level':'Level',
            'enabled':'bool',
            'id':'int',
            'type__title':'str',
    })
    AlertserviceUpdateReturns = typing.TypedDict('AlertserviceUpdateReturns', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'level':'Level',
            'enabled':'bool',
            'id':'int',
            'type__title':'str',
    })
    class Level(str,Enum):
        INFO = 'INFO'
        NOTICE = 'NOTICE'
        WARNING = 'WARNING'
        ERROR = 'ERROR'
        CRITICAL = 'CRITICAL'
        ALERT = 'ALERT'
        EMERGENCY = 'EMERGENCY'
        ...
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
