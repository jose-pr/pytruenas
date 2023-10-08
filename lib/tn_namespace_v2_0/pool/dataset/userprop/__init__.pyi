
from pytruenas import Namespace, TrueNASClient
import typing
class PoolDatasetUserprop(Namespace):
    _namespace:typing.Literal['pool.dataset.userprop']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        dataset_user_prop_create:'DatasetUserPropCreate'={},
    /) -> 'PoolDatasetUserpropCreateReturns': 
        """
        Create a user property for a given `id` dataset.

        Parameters
        ----------
        dataset_user_prop_create:
            dataset_user_prop_create
        Returns
        -------
        PoolDatasetUserpropCreateReturns:
            pool_dataset_userprop_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'str',
        dataset_user_prop_delete:'DatasetUserPropDelete'={},
    /) -> 'bool': 
        """
        Delete user property `dataset_user_prop_delete.name` for `id` dataset.

        Parameters
        ----------
        id:
            id
        dataset_user_prop_delete:
            dataset_user_prop_delete
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
    /) -> 'list[PoolDatasetUserpropEntry]|PoolDatasetUserpropEntry|int|PoolDatasetUserpropEntry': 
        """
        Query all user properties for ZFS datasets.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list[PoolDatasetUserpropEntry]:
            
        PoolDatasetUserpropEntry:
            
        int:
            
        PoolDatasetUserpropEntry:
            
        """
        ...
    @typing.overload
    def update(self, 
        id:'str',
        dataset_user_prop_update:'DatasetUserPropUpdate'={},
    /) -> 'PoolDatasetUserpropUpdateReturns': 
        """
        Update `dataset_user_prop_update.name` user property for `id` dataset.

        Parameters
        ----------
        id:
            id
        dataset_user_prop_update:
            dataset_user_prop_update
        Returns
        -------
        PoolDatasetUserpropUpdateReturns:
            pool_dataset_userprop_update_returns
        """
        ...

class DatasetUserPropCreate(typing.TypedDict):
        id:'str'
        property:'Property'
        ...
class Property(typing.TypedDict):
        name:'str'
        value:'str'
        ...
class PoolDatasetUserpropCreateReturns(typing.TypedDict):
        id:'str'
        properties:'dict[str]'
        ...
class DatasetUserPropDelete(typing.TypedDict):
        name:'str'
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
class PoolDatasetUserpropEntry(typing.TypedDict):
        id:'str'
        properties:'dict[str]'
        ...
class DatasetUserPropUpdate(typing.TypedDict):
        name:'str'
        value:'str'
        ...
class PoolDatasetUserpropUpdateReturns(typing.TypedDict):
        id:'str'
        properties:'dict[str]'
        ...
