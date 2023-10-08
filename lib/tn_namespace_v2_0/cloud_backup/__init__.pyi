
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Cloud_backup(Namespace):
    _namespace:_ty.Literal['cloud_backup']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def abort(self, 
        id:'int',
    /) -> None: 
        """
        Aborts cloud backup task.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        """
        ...
    @_ty.overload
    def create(self, 
        cloud_backup_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        

        Parameters
        ----------
        cloud_backup_create:
            cloud_backup_create
        Returns
        -------
        dict[str]:
            cloud_backup_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Deletes cloud backup entry `id`.

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
    def init(self, 
        id:'int',
    /) -> None: 
        """
        Initializes the repository for the cloud backup job `id`.

        Parameters
        ----------
        id:
            id
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
    def sync(self, 
        id:'int',
        cloud_backup_sync_options:'dict[str]'={},
    /) -> None: 
        """
        Run the cloud backup job `id`.

        Parameters
        ----------
        id:
            id
        cloud_backup_sync_options:
            cloud_backup_sync_options
        Returns
        -------
        """
        ...
    @_ty.overload
    def update(self, 
        id:'int',
        cloud_backup_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Updates the cloud backup entry `id` with `data`.

        Parameters
        ----------
        id:
            id
        cloud_backup_update:
            cloud_backup_update
        Returns
        -------
        dict[str]:
            cloud_backup_update_returns
        """
        ...
