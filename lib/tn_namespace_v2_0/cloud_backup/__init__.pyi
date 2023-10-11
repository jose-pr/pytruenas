
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Cloud_backup(
    Namespace
    ):
    _namespace:typing.Literal['cloud_backup']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def abort(self, 
        _id:'int',
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
    @typing.overload
    def create(self, 
        _cloud_backup_create:'CloudBackupCreate',
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
    @typing.overload
    def delete(self, 
        _id:'int',
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
    def init(self, 
        _id:'int',
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
    def sync(self, 
        _id:'int',
        _cloud_backup_sync_options:'CloudBackupSyncOptions',
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
    @typing.overload
    def update(self, 
        _id:'int',
        _cloud_backup_update:'CloudBackupUpdate',
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
    CloudBackupCreate = typing.TypedDict('CloudBackupCreate', {
            'description':'str',
            'path':'str',
            'credentials':'int',
            'attributes':'dict[str]',
            'schedule':'Schedule',
            'pre_script':'str',
            'post_script':'str',
            'snapshot':'bool',
            'bwlimit':'list[CloudSyncBwlimit]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'password':'str',
    })
    CloudBackupSyncOptions = typing.TypedDict('CloudBackupSyncOptions', {
            'dry_run':'bool',
    })
    CloudBackupUpdate = typing.TypedDict('CloudBackupUpdate', {
            'description':'str',
            'path':'str',
            'credentials':'int',
            'attributes':'dict[str]',
            'schedule':'Schedule',
            'pre_script':'str',
            'post_script':'str',
            'snapshot':'bool',
            'bwlimit':'list[CloudSyncBwlimit]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'password':'str',
    })
    CloudSyncBwlimit = typing.TypedDict('CloudSyncBwlimit', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
