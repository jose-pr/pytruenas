
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Cloudsync(
    Namespace
    ):
    _namespace:typing.Literal['cloudsync']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def abort(self, 
        _id:'int',
    /) -> None: 
        """
        Aborts cloud sync task.

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
        _cloud_sync_create:'CloudSyncCreate',
    /) -> 'dict[str]': 
        """
        Creates a new cloud_sync entry.

        Parameters
        ----------
        cloud_sync_create:
            cloud_sync_create
        Returns
        -------
        dict[str]:
            cloudsync_create_returns
        """
        ...
    @typing.overload
    def create_bucket(self, 
        _credentials_id:'int',
        _name:'str',
    /) -> None: 
        """
        Creates a new bucket `name` using ` credentials_id`.

        Parameters
        ----------
        credentials_id:
            credentials_id
        name:
            name
        Returns
        -------
        """
        ...
    @typing.overload
    def delete(self, 
        _id:'int',
    /) -> 'bool': 
        """
        Deletes cloud_sync entry `id`.

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
    def list_buckets(self, 
        _credentials_id:'int',
    /) -> None: 
        """
        

        Parameters
        ----------
        credentials_id:
            credentials_id
        Returns
        -------
        """
        ...
    @typing.overload
    def list_directory(self, 
        _cloud_sync_ls:'CloudSyncLs',
    /) -> None: 
        """
        List contents of a remote bucket / directory.
        
        If remote supports buckets, path is constructed by two keys "bucket"/"folder" in `attributes`.
        If remote does not support buckets, path is constructed using "folder" key only in `attributes`.
        "folder" is directory name and "bucket" is bucket name for remote.
        
        Path examples:
        
        S3 Service
        `bucketname/directory/name`
        
        Dropbox Service
        `directory/name`
        
        `credentials` is a valid id of a Cloud Sync Credential which will be used to connect to the provider.

        Parameters
        ----------
        cloud_sync_ls:
            cloud_sync_ls
        Returns
        -------
        """
        ...
    @typing.overload
    def providers(self, 
    /) -> None: 
        """
        Returns a list of dictionaries of supported providers for Cloud Sync Tasks.
        
        `credentials_schema` is JSON schema for credentials attributes.
        
        `task_schema` is JSON schema for task attributes.
        
        `buckets` is a boolean value which is set to "true" if provider supports buckets.
        
        Example of a single provider:
        
        [
            {
                "name": "AMAZON_CLOUD_DRIVE",
                "title": "Amazon Cloud Drive",
                "credentials_schema": [
                    {
                        "property": "client_id",
                        "schema": {
                            "title": "Amazon Application Client ID",
                            "_required_": true,
                            "type": "string"
                        }
                    },
                    {
                        "property": "client_secret",
                        "schema": {
                            "title": "Application Key",
                            "_required_": true,
                            "type": "string"
                        }
                    }
                ],
                "credentials_oauth": null,
                "buckets": false,
                "bucket_title": "Bucket",
                "task_schema": []
            }
        ]

        Parameters
        ----------
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
    def restore(self, 
        _id:'int',
        _cloud_sync_restore:'CloudSyncRestore',
    /) -> None: 
        """
        Create the opposite of cloud sync task `id` (PULL if it was PUSH and vice versa).

        Parameters
        ----------
        id:
            id
        cloud_sync_restore:
            cloud_sync_restore
        Returns
        -------
        """
        ...
    @typing.overload
    def sync(self, 
        _id:'int',
        _cloud_sync_sync_options:'CloudSyncSyncOptions',
    /) -> None: 
        """
        Run the cloud_sync job `id`, syncing the local data to remote.

        Parameters
        ----------
        id:
            id
        cloud_sync_sync_options:
            cloud_sync_sync_options
        Returns
        -------
        """
        ...
    @typing.overload
    def sync_onetime(self, 
        _cloud_sync_sync_onetime:'CloudSyncSyncOnetime',
        _cloud_sync_sync_onetime_options:'CloudSyncSyncOnetimeOptions',
    /) -> None: 
        """
        Run cloud sync task without creating it.

        Parameters
        ----------
        cloud_sync_sync_onetime:
            cloud_sync_sync_onetime
        cloud_sync_sync_onetime_options:
            cloud_sync_sync_onetime_options
        Returns
        -------
        """
        ...
    @typing.overload
    def update(self, 
        _id:'int',
        _cloud_sync_update:'CloudSyncUpdate',
    /) -> 'dict[str]': 
        """
        Updates the cloud_sync entry `id` with `data`.

        Parameters
        ----------
        id:
            Updates the cloud_sync entry `id` with `data`.
            Creates a new cloud_sync entry.
        cloud_sync_update:
            cloud_sync_update
        Returns
        -------
        dict[str]:
            cloudsync_update_returns
        """
        ...
    CloudSyncBwlimit = typing.TypedDict('CloudSyncBwlimit', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
    })
    CloudSyncCreate = typing.TypedDict('CloudSyncCreate', {
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
            'direction':'Direction',
            'transfer_mode':'TransferMode',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
    })
    CloudSyncLs = typing.TypedDict('CloudSyncLs', {
            'credentials':'int',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'attributes':'dict[str]',
            'args':'str',
    })
    CloudSyncRestore = typing.TypedDict('CloudSyncRestore', {
            'description':'str',
            'transfer_mode':'TransferMode_',
            'path':'str',
    })
    CloudSyncSyncOnetime = typing.TypedDict('CloudSyncSyncOnetime', {
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
            'direction':'Direction',
            'transfer_mode':'TransferMode',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
    })
    CloudSyncSyncOnetimeOptions = typing.TypedDict('CloudSyncSyncOnetimeOptions', {
            'dry_run':'bool',
    })
    CloudSyncSyncOptions = typing.TypedDict('CloudSyncSyncOptions', {
            'dry_run':'bool',
    })
    CloudSyncUpdate = typing.TypedDict('CloudSyncUpdate', {
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
            'direction':'Direction',
            'transfer_mode':'TransferMode',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
    })
    class Direction(str,Enum):
        PUSH = 'PUSH'
        PULL = 'PULL'
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
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    class TransferMode(str,Enum):
        SYNC = 'SYNC'
        COPY = 'COPY'
        MOVE = 'MOVE'
        ...
    class TransferMode_(str,Enum):
        SYNC = 'SYNC'
        COPY = 'COPY'
        ...
