
from pytruenas import Namespace, TrueNASClient
import typing
class Api_key(Namespace):
    _namespace:typing.Literal['api_key']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        api_key_create:'ApiKeyCreate'={},
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
    AllowlistItem = typing.TypedDict('AllowlistItem', {
            'method':'str',
            'resource':'str',
    })
    ApiKeyCreate = typing.TypedDict('ApiKeyCreate', {
            'name':'str',
            'allowlist':'list[AllowlistItem]',
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
    ApiKeyUpdate = typing.TypedDict('ApiKeyUpdate', {
            'name':'str',
            'allowlist':'list[AllowlistItem]',
            'reset':'bool',
    })
    @typing.overload
    def delete(self, 
        id:'int',
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
    AllowlistItem = typing.TypedDict('AllowlistItem', {
            'method':'str',
            'resource':'str',
    })
    ApiKeyCreate = typing.TypedDict('ApiKeyCreate', {
            'name':'str',
            'allowlist':'list[AllowlistItem]',
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
    ApiKeyUpdate = typing.TypedDict('ApiKeyUpdate', {
            'name':'str',
            'allowlist':'list[AllowlistItem]',
            'reset':'bool',
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
    AllowlistItem = typing.TypedDict('AllowlistItem', {
            'method':'str',
            'resource':'str',
    })
    ApiKeyCreate = typing.TypedDict('ApiKeyCreate', {
            'name':'str',
            'allowlist':'list[AllowlistItem]',
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
    ApiKeyUpdate = typing.TypedDict('ApiKeyUpdate', {
            'name':'str',
            'allowlist':'list[AllowlistItem]',
            'reset':'bool',
    })
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'typing.Union[list[dict[str]], dict[str], int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[dict[str]], dict[str], int]:
            
        """
        ...
    AllowlistItem = typing.TypedDict('AllowlistItem', {
            'method':'str',
            'resource':'str',
    })
    ApiKeyCreate = typing.TypedDict('ApiKeyCreate', {
            'name':'str',
            'allowlist':'list[AllowlistItem]',
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
    ApiKeyUpdate = typing.TypedDict('ApiKeyUpdate', {
            'name':'str',
            'allowlist':'list[AllowlistItem]',
            'reset':'bool',
    })
    @typing.overload
    def update(self, 
        id:'int',
        api_key_update:'ApiKeyUpdate'={},
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
            'method':'str',
            'resource':'str',
    })
    ApiKeyCreate = typing.TypedDict('ApiKeyCreate', {
            'name':'str',
            'allowlist':'list[AllowlistItem]',
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
    ApiKeyUpdate = typing.TypedDict('ApiKeyUpdate', {
            'name':'str',
            'allowlist':'list[AllowlistItem]',
            'reset':'bool',
    })

