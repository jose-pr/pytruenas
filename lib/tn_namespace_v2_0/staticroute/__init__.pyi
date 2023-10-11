
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Staticroute(
    Namespace
    ):
    _namespace:typing.Literal['staticroute']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        _staticroute_create:'StaticrouteCreate',
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
    @typing.overload
    def delete(self, 
        _id:'int',
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
    def query(self, 
        _query_filters:'list[list]',
        _query_options:'QueryOptions',
    /) -> 'typing.Union[list[StaticrouteEntry], StaticrouteEntry, int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[StaticrouteEntry], StaticrouteEntry, int]:
            
        """
        ...
    @typing.overload
    def update(self, 
        _id:'int',
        _staticroute_update:'StaticrouteUpdate',
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
