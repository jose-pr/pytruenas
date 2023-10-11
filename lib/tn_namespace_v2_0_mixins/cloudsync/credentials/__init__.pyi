
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin
from enum import Enum
import typing
class CloudsyncCredentials(
    TableExtMixin,
    Namespace
    ):
    _namespace:typing.Literal['cloudsync.credentials']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        cloud_sync_credentials_create:'CloudSyncCredentialsCreate',
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
    @typing.overload
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
    @typing.overload
    def get_instance(self, 
        id:'typing.Union[str, int, bool, dict[str], list]',
        query_options_get_instance:'QueryOptionsGetInstance',
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
        query_filters:'list[list]',
        query_options:'QueryOptions',
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
        id:'int',
        cloud_sync_credentials_update:'CloudSyncCredentialsUpdate',
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
    @typing.overload
    def verify(self, 
        cloud_sync_credentials_verify:'CloudSyncCredentialsVerify',
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
    CloudSyncCredentialsCreate = typing.TypedDict('CloudSyncCredentialsCreate', {
            'name':'str',
            'provider':'str',
            'attributes':'dict[str]',
    })
    CloudSyncCredentialsUpdate = typing.TypedDict('CloudSyncCredentialsUpdate', {
            'name':'str',
            'provider':'str',
            'attributes':'dict[str]',
    })
    CloudSyncCredentialsVerify = typing.TypedDict('CloudSyncCredentialsVerify', {
            'provider':'str',
            'attributes':'dict[str]',
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
