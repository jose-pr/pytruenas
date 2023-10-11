
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin
from enum import Enum
import typing
class Api_key(
    TableExtMixin,
    Namespace
    ):
    _namespace:typing.Literal['api_key']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        _api_key_create:'ApiKeyCreate',
    /) -> 'dict[str]': 
        """
        Creates API Key.
        
        `name` is a user-readable name for key.

        Parameters
        ----------
        api_key_create:
            api_key_create
        Returns
        -------
        dict[str]:
            api_key_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        _id:'int',
    /) -> 'bool': 
        """
        Delete API Key `id`.

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
    /) -> 'typing.Union[list, dict[str], int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list, dict[str], int]:
            
        """
        ...
    @typing.overload
    def update(self, 
        _id:'int',
        _api_key_update:'ApiKeyUpdate',
    /) -> 'dict[str]': 
        """
        Update API Key `id`.
        
        Specify `reset: true` to reset this API Key.

        Parameters
        ----------
        id:
            Update API Key `id`.
        api_key_update:
            api_key_update
        Returns
        -------
        dict[str]:
            api_key_update_returns
        """
        ...
    AllowlistItem = typing.TypedDict('AllowlistItem', {
            'method':'Method',
            'resource':'str',
    })
    ApiKeyCreate = typing.TypedDict('ApiKeyCreate', {
            'name':'str',
            'allowlist':'list[AllowlistItem]',
    })
    ApiKeyUpdate = typing.TypedDict('ApiKeyUpdate', {
            'name':'str',
            'allowlist':'list[AllowlistItem]',
            'reset':'bool',
    })
    class Method(str,Enum):
        GET = 'GET'
        POST = 'POST'
        PUT = 'PUT'
        DELETE = 'DELETE'
        CALL = 'CALL'
        SUBSCRIBE = 'SUBSCRIBE'
        All = '*'
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
