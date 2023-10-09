
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
class Staticroute(
    TableExtMixin,
    Namespace
    ):
    _namespace:typing.Literal['staticroute']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        staticroute_create:'StaticrouteCreate'={},
    /) -> 'StaticrouteCreateReturns': 
        """
        Create a Static Route.
        
        Address families of `gateway` and `destination` should match when creating a static route.
        
        `description` is an optional attribute for any notes regarding the static route.

        Parameters
        ----------
        staticroute_create:
            staticroute_create
        Returns
        -------
        StaticrouteCreateReturns:
            staticroute_create_returns
        """
        ...
    StaticrouteCreate = typing.TypedDict('StaticrouteCreate', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
    })
    StaticrouteCreateReturns = typing.TypedDict('StaticrouteCreateReturns', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
            'id':'int',
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
    StaticrouteEntry = typing.TypedDict('StaticrouteEntry', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
            'id':'int',
    })
    StaticrouteUpdate = typing.TypedDict('StaticrouteUpdate', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
    })
    StaticrouteUpdateReturns = typing.TypedDict('StaticrouteUpdateReturns', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
            'id':'int',
    })
    @typing.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete Static Route of `id`.

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
    StaticrouteCreate = typing.TypedDict('StaticrouteCreate', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
    })
    StaticrouteCreateReturns = typing.TypedDict('StaticrouteCreateReturns', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
            'id':'int',
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
    StaticrouteEntry = typing.TypedDict('StaticrouteEntry', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
            'id':'int',
    })
    StaticrouteUpdate = typing.TypedDict('StaticrouteUpdate', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
    })
    StaticrouteUpdateReturns = typing.TypedDict('StaticrouteUpdateReturns', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
            'id':'int',
    })
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
    StaticrouteCreate = typing.TypedDict('StaticrouteCreate', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
    })
    StaticrouteCreateReturns = typing.TypedDict('StaticrouteCreateReturns', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
            'id':'int',
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
    StaticrouteEntry = typing.TypedDict('StaticrouteEntry', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
            'id':'int',
    })
    StaticrouteUpdate = typing.TypedDict('StaticrouteUpdate', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
    })
    StaticrouteUpdateReturns = typing.TypedDict('StaticrouteUpdateReturns', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
            'id':'int',
    })
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'typing.Union[list[StaticrouteEntry], ForwardRef(StaticrouteEntry), int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[StaticrouteEntry], ForwardRef(StaticrouteEntry), int]:
            
        """
        ...
    StaticrouteCreate = typing.TypedDict('StaticrouteCreate', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
    })
    StaticrouteCreateReturns = typing.TypedDict('StaticrouteCreateReturns', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
            'id':'int',
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
    StaticrouteEntry = typing.TypedDict('StaticrouteEntry', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
            'id':'int',
    })
    StaticrouteUpdate = typing.TypedDict('StaticrouteUpdate', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
    })
    StaticrouteUpdateReturns = typing.TypedDict('StaticrouteUpdateReturns', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
            'id':'int',
    })
    @typing.overload
    def update(self, 
        id:'int',
        staticroute_update:'StaticrouteUpdate'={},
    /) -> 'StaticrouteUpdateReturns': 
        """
        Update Static Route of `id`.

        Parameters
        ----------
        id:
            Update Static Route of `id`.
            Create a Static Route.
        staticroute_update:
            staticroute_update
        Returns
        -------
        StaticrouteUpdateReturns:
            staticroute_update_returns
        """
        ...
    StaticrouteCreate = typing.TypedDict('StaticrouteCreate', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
    })
    StaticrouteCreateReturns = typing.TypedDict('StaticrouteCreateReturns', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
            'id':'int',
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
    StaticrouteEntry = typing.TypedDict('StaticrouteEntry', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
            'id':'int',
    })
    StaticrouteUpdate = typing.TypedDict('StaticrouteUpdate', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
    })
    StaticrouteUpdateReturns = typing.TypedDict('StaticrouteUpdateReturns', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
            'id':'int',
    })
