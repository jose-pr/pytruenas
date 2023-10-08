
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class CloudsyncCredentials(Namespace):
    _namespace:_ty.Literal['cloudsync.credentials']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        cloud_sync_credentials_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create Cloud Sync Credentials.
        
        `attributes` is a dictionary of valid values which will be used to authorize with the `provider`.

        Parameters
        ----------
        cloud_sync_credentials_create:
            cloud_sync_credentials_create
        Returns
        -------
        dict[str]:
            cloudsync_credentials_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete Cloud Sync Credentials of `id`.

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
    def update(self, 
        id:'int',
        cloud_sync_credentials_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update Cloud Sync Credentials of `id`.

        Parameters
        ----------
        id:
            Update Cloud Sync Credentials of `id`.
            Create Cloud Sync Credentials.
        cloud_sync_credentials_update:
            cloud_sync_credentials_update
        Returns
        -------
        dict[str]:
            cloudsync_credentials_update_returns
        """
        ...
    @_ty.overload
    def verify(self, 
        cloud_sync_credentials_verify:'dict[str]'={},
    /) -> None: 
        """
        Verify if `attributes` provided for `provider` are authorized by the `provider`.

        Parameters
        ----------
        cloud_sync_credentials_verify:
            cloud_sync_credentials_verify
        Returns
        -------
        """
        ...
