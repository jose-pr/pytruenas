
from pytruenas import Namespace, TrueNASClient
import typing
class Cloudsync(Namespace):
    _namespace:typing.Literal['cloudsync']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def abort(self, 
        id:'int',
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
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
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
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
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
    CloudSyncLs = typing.TypedDict('CloudSyncLs', {
            'credentials':'int',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'attributes':'dict[str]',
            'args':'str',
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
    CloudSyncRestore = typing.TypedDict('CloudSyncRestore', {
            'description':'str',
            'transfer_mode':'str',
            'path':'str',
    })
    CloudSyncSyncOptions = typing.TypedDict('CloudSyncSyncOptions', {
            'dry_run':'bool',
    })
    CloudSyncBwlimit_ = typing.TypedDict('CloudSyncBwlimit_', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit_]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
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
    CloudSyncBwlimit__ = typing.TypedDict('CloudSyncBwlimit__', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit__]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
    })
    @typing.overload
    def create(self, 
        cloud_sync_create:'CloudSyncCreate'={},
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
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
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
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
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
    CloudSyncLs = typing.TypedDict('CloudSyncLs', {
            'credentials':'int',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'attributes':'dict[str]',
            'args':'str',
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
    CloudSyncRestore = typing.TypedDict('CloudSyncRestore', {
            'description':'str',
            'transfer_mode':'str',
            'path':'str',
    })
    CloudSyncSyncOptions = typing.TypedDict('CloudSyncSyncOptions', {
            'dry_run':'bool',
    })
    CloudSyncBwlimit_ = typing.TypedDict('CloudSyncBwlimit_', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit_]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
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
    CloudSyncBwlimit__ = typing.TypedDict('CloudSyncBwlimit__', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit__]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
    })
    @typing.overload
    def create_bucket(self, 
        credentials_id:'int',
        name:'str',
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
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
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
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
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
    CloudSyncLs = typing.TypedDict('CloudSyncLs', {
            'credentials':'int',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'attributes':'dict[str]',
            'args':'str',
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
    CloudSyncRestore = typing.TypedDict('CloudSyncRestore', {
            'description':'str',
            'transfer_mode':'str',
            'path':'str',
    })
    CloudSyncSyncOptions = typing.TypedDict('CloudSyncSyncOptions', {
            'dry_run':'bool',
    })
    CloudSyncBwlimit_ = typing.TypedDict('CloudSyncBwlimit_', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit_]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
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
    CloudSyncBwlimit__ = typing.TypedDict('CloudSyncBwlimit__', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit__]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
    })
    @typing.overload
    def delete(self, 
        id:'int',
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
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
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
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
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
    CloudSyncLs = typing.TypedDict('CloudSyncLs', {
            'credentials':'int',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'attributes':'dict[str]',
            'args':'str',
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
    CloudSyncRestore = typing.TypedDict('CloudSyncRestore', {
            'description':'str',
            'transfer_mode':'str',
            'path':'str',
    })
    CloudSyncSyncOptions = typing.TypedDict('CloudSyncSyncOptions', {
            'dry_run':'bool',
    })
    CloudSyncBwlimit_ = typing.TypedDict('CloudSyncBwlimit_', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit_]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
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
    CloudSyncBwlimit__ = typing.TypedDict('CloudSyncBwlimit__', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit__]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
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
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
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
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
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
    CloudSyncLs = typing.TypedDict('CloudSyncLs', {
            'credentials':'int',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'attributes':'dict[str]',
            'args':'str',
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
    CloudSyncRestore = typing.TypedDict('CloudSyncRestore', {
            'description':'str',
            'transfer_mode':'str',
            'path':'str',
    })
    CloudSyncSyncOptions = typing.TypedDict('CloudSyncSyncOptions', {
            'dry_run':'bool',
    })
    CloudSyncBwlimit_ = typing.TypedDict('CloudSyncBwlimit_', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit_]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
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
    CloudSyncBwlimit__ = typing.TypedDict('CloudSyncBwlimit__', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit__]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
    })
    @typing.overload
    def list_buckets(self, 
        credentials_id:'int',
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
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
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
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
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
    CloudSyncLs = typing.TypedDict('CloudSyncLs', {
            'credentials':'int',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'attributes':'dict[str]',
            'args':'str',
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
    CloudSyncRestore = typing.TypedDict('CloudSyncRestore', {
            'description':'str',
            'transfer_mode':'str',
            'path':'str',
    })
    CloudSyncSyncOptions = typing.TypedDict('CloudSyncSyncOptions', {
            'dry_run':'bool',
    })
    CloudSyncBwlimit_ = typing.TypedDict('CloudSyncBwlimit_', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit_]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
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
    CloudSyncBwlimit__ = typing.TypedDict('CloudSyncBwlimit__', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit__]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
    })
    @typing.overload
    def list_directory(self, 
        cloud_sync_ls:'CloudSyncLs'={},
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
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
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
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
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
    CloudSyncLs = typing.TypedDict('CloudSyncLs', {
            'credentials':'int',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'attributes':'dict[str]',
            'args':'str',
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
    CloudSyncRestore = typing.TypedDict('CloudSyncRestore', {
            'description':'str',
            'transfer_mode':'str',
            'path':'str',
    })
    CloudSyncSyncOptions = typing.TypedDict('CloudSyncSyncOptions', {
            'dry_run':'bool',
    })
    CloudSyncBwlimit_ = typing.TypedDict('CloudSyncBwlimit_', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit_]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
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
    CloudSyncBwlimit__ = typing.TypedDict('CloudSyncBwlimit__', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit__]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
    })
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
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
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
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
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
    CloudSyncLs = typing.TypedDict('CloudSyncLs', {
            'credentials':'int',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'attributes':'dict[str]',
            'args':'str',
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
    CloudSyncRestore = typing.TypedDict('CloudSyncRestore', {
            'description':'str',
            'transfer_mode':'str',
            'path':'str',
    })
    CloudSyncSyncOptions = typing.TypedDict('CloudSyncSyncOptions', {
            'dry_run':'bool',
    })
    CloudSyncBwlimit_ = typing.TypedDict('CloudSyncBwlimit_', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit_]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
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
    CloudSyncBwlimit__ = typing.TypedDict('CloudSyncBwlimit__', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit__]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
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
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
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
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
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
    CloudSyncLs = typing.TypedDict('CloudSyncLs', {
            'credentials':'int',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'attributes':'dict[str]',
            'args':'str',
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
    CloudSyncRestore = typing.TypedDict('CloudSyncRestore', {
            'description':'str',
            'transfer_mode':'str',
            'path':'str',
    })
    CloudSyncSyncOptions = typing.TypedDict('CloudSyncSyncOptions', {
            'dry_run':'bool',
    })
    CloudSyncBwlimit_ = typing.TypedDict('CloudSyncBwlimit_', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit_]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
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
    CloudSyncBwlimit__ = typing.TypedDict('CloudSyncBwlimit__', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit__]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
    })
    @typing.overload
    def restore(self, 
        id:'int',
        cloud_sync_restore:'CloudSyncRestore'={},
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
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
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
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
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
    CloudSyncLs = typing.TypedDict('CloudSyncLs', {
            'credentials':'int',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'attributes':'dict[str]',
            'args':'str',
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
    CloudSyncRestore = typing.TypedDict('CloudSyncRestore', {
            'description':'str',
            'transfer_mode':'str',
            'path':'str',
    })
    CloudSyncSyncOptions = typing.TypedDict('CloudSyncSyncOptions', {
            'dry_run':'bool',
    })
    CloudSyncBwlimit_ = typing.TypedDict('CloudSyncBwlimit_', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit_]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
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
    CloudSyncBwlimit__ = typing.TypedDict('CloudSyncBwlimit__', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit__]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
    })
    @typing.overload
    def sync(self, 
        id:'int',
        cloud_sync_sync_options:'CloudSyncSyncOptions'={},
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
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
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
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
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
    CloudSyncLs = typing.TypedDict('CloudSyncLs', {
            'credentials':'int',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'attributes':'dict[str]',
            'args':'str',
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
    CloudSyncRestore = typing.TypedDict('CloudSyncRestore', {
            'description':'str',
            'transfer_mode':'str',
            'path':'str',
    })
    CloudSyncSyncOptions = typing.TypedDict('CloudSyncSyncOptions', {
            'dry_run':'bool',
    })
    CloudSyncBwlimit_ = typing.TypedDict('CloudSyncBwlimit_', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit_]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
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
    CloudSyncBwlimit__ = typing.TypedDict('CloudSyncBwlimit__', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit__]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
    })
    @typing.overload
    def sync_onetime(self, 
        cloud_sync_sync_onetime:'CloudSyncSyncOnetime'={},
        cloud_sync_sync_onetime_options:'CloudSyncSyncOnetimeOptions'={},
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
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
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
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
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
    CloudSyncLs = typing.TypedDict('CloudSyncLs', {
            'credentials':'int',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'attributes':'dict[str]',
            'args':'str',
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
    CloudSyncRestore = typing.TypedDict('CloudSyncRestore', {
            'description':'str',
            'transfer_mode':'str',
            'path':'str',
    })
    CloudSyncSyncOptions = typing.TypedDict('CloudSyncSyncOptions', {
            'dry_run':'bool',
    })
    CloudSyncBwlimit_ = typing.TypedDict('CloudSyncBwlimit_', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit_]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
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
    CloudSyncBwlimit__ = typing.TypedDict('CloudSyncBwlimit__', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit__]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
    })
    @typing.overload
    def update(self, 
        id:'int',
        cloud_sync_update:'CloudSyncUpdate'={},
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
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
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
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
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
    CloudSyncLs = typing.TypedDict('CloudSyncLs', {
            'credentials':'int',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'attributes':'dict[str]',
            'args':'str',
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
    CloudSyncRestore = typing.TypedDict('CloudSyncRestore', {
            'description':'str',
            'transfer_mode':'str',
            'path':'str',
    })
    CloudSyncSyncOptions = typing.TypedDict('CloudSyncSyncOptions', {
            'dry_run':'bool',
    })
    CloudSyncBwlimit_ = typing.TypedDict('CloudSyncBwlimit_', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit_]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
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
    CloudSyncBwlimit__ = typing.TypedDict('CloudSyncBwlimit__', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
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
            'bwlimit':'list[CloudSyncBwlimit__]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'str',
            'transfer_mode':'str',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
    })

