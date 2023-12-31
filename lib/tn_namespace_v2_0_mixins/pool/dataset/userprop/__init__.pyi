
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin
from enum import Enum
import typing
class PoolDatasetUserprop(
    TableExtMixin,
    Namespace
    ):
    _namespace:typing.Literal['pool.dataset.userprop']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        _dataset_user_prop_create:'DatasetUserPropCreate',
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
        _id:'str',
        _dataset_user_prop_delete:'DatasetUserPropDelete',
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
    /) -> 'typing.Union[list[PoolDatasetUserpropEntry], PoolDatasetUserpropEntry, int]': 
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
        typing.Union[list[PoolDatasetUserpropEntry], PoolDatasetUserpropEntry, int]:
            
        """
        ...
    @typing.overload
    def update(self, 
        _id:'str',
        _dataset_user_prop_update:'DatasetUserPropUpdate',
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
    DatasetUserPropCreate = typing.TypedDict('DatasetUserPropCreate', {
            'id':'str',
            'property':'Property',
    })
    DatasetUserPropDelete = typing.TypedDict('DatasetUserPropDelete', {
            'name':'str',
    })
    DatasetUserPropUpdate = typing.TypedDict('DatasetUserPropUpdate', {
            'name':'str',
            'value':'str',
    })
    PoolDatasetUserpropCreateReturns = typing.TypedDict('PoolDatasetUserpropCreateReturns', {
            'id':'str',
            'properties':'dict[str]',
    })
    PoolDatasetUserpropEntry = typing.TypedDict('PoolDatasetUserpropEntry', {
            'id':'str',
            'properties':'dict[str]',
    })
    PoolDatasetUserpropUpdateReturns = typing.TypedDict('PoolDatasetUserpropUpdateReturns', {
            'id':'str',
            'properties':'dict[str]',
    })
    Property = typing.TypedDict('Property', {
            'name':'str',
            'value':'str',
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
