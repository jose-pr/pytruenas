
from pytruenas import Namespace, TrueNASClient
import typing
class Cloud_backup(Namespace):
    _namespace:typing.Literal['cloud_backup']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
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
    @typing.overload
    def create(self, 
        cloud_backup_create:'CloudBackupCreate'={},
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
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'list[dict[str]]|dict[str]|int|dict[str]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list[dict[str]]:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @typing.overload
    def sync(self, 
        id:'int',
        cloud_backup_sync_options:'CloudBackupSyncOptions'={},
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
        id:'int',
        cloud_backup_update:'CloudBackupUpdate'={},
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

class CloudBackupCreate(typing.TypedDict):
        description:'str'
        path:'str'
        credentials:'int'
        attributes:'dict[str]'
        schedule:'Schedule'
        pre_script:'str'
        post_script:'str'
        snapshot:'bool'
        bwlimit:'list[CloudSyncBwlimit]'
        include:'list[str]'
        exclude:'list[str]'
        transfers:'typing.Optional[int]'
        args:'str'
        enabled:'bool'
        password:'str'
        ...
class Schedule(typing.TypedDict):
        minute:'str'
        hour:'str'
        dom:'str'
        month:'str'
        dow:'str'
        ...
class CloudSyncBwlimit(typing.TypedDict):
        time:'str'
        bandwidth:'typing.Optional[int]'
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
class CloudBackupSyncOptions(typing.TypedDict):
        dry_run:'bool'
        ...
class CloudBackupUpdate(typing.TypedDict):
        description:'str'
        path:'str'
        credentials:'int'
        attributes:'dict[str]'
        schedule:'Schedule'
        pre_script:'str'
        post_script:'str'
        snapshot:'bool'
        bwlimit:'list[CloudSyncBwlimit]'
        include:'list[str]'
        exclude:'list[str]'
        transfers:'typing.Optional[int]'
        args:'str'
        enabled:'bool'
        password:'str'
        ...
