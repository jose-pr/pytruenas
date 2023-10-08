
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class PoolDatasetUserprop(Namespace):
    _namespace:_ty.Literal['pool.dataset.userprop']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        dataset_user_prop_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create a user property for a given `id` dataset.

        Parameters
        ----------
        dataset_user_prop_create:
            dataset_user_prop_create
        Returns
        -------
        dict[str]:
            pool_dataset_userprop_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'str',
        dataset_user_prop_delete:'dict[str]'={},
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
        Query all user properties for ZFS datasets.

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
    def update(self, 
        id:'str',
        dataset_user_prop_update:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            pool_dataset_userprop_update_returns
        """
        ...
