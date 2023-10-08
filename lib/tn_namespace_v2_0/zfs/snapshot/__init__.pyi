
from pytruenas import Namespace, TrueNASClient
import typing
class ZfsSnapshot(Namespace):
    _namespace:typing.Literal['zfs.snapshot']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def clone(self, 
        snapshot_clone:'SnapshotClone'={},
    /) -> None: 
        """
        Clone a given snapshot to a new dataset.
        
        Returns:
            bool: True if succeed otherwise False.

        Parameters
        ----------
        snapshot_clone:
            snapshot_clone
        Returns
        -------
        """
        ...
    @typing.overload
    def create(self, 
        snapshot_create:'SnapshotCreate'={},
    /) -> 'dict[str]': 
        """
        Take a snapshot from a given dataset.

        Parameters
        ----------
        snapshot_create:
            snapshot_create
        Returns
        -------
        dict[str]:
            zfs_snapshot_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'str',
        options:'Options'={},
    /) -> 'bool': 
        """
        Delete snapshot of name `id`.
        
        `options.defer` will defer the deletion of snapshot.

        Parameters
        ----------
        id:
            Delete snapshot of name `id`.
        options:
            options
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
    def hold(self, 
        id:'str',
        options:'Options_'={},
    /) -> None: 
        """
        Holds snapshot `id`.
        
        `truenas` tag will be added to the snapshot's tag namespace.
        
        `options.recursive` will hold snapshots recursively.

        Parameters
        ----------
        id:
            Holds snapshot `id`.
        options:
            options
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
        Query all ZFS Snapshots with `query-filters` and `query-options`.
        
        `query-options.extra.holds` specifies whether hold tags for snapshots should be retrieved (false by default)
        
        `query-options.extra.min_txg` can be specified to limit snapshot retrieval based on minimum transaction group.
        
        `query-options.extra.max_txg` can be specified to limit snapshot retrieval based on maximum transaction group.

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
    def release(self, 
        id:'str',
        options:'Options_'={},
    /) -> None: 
        """
        Release held snapshot `id`.
        
        Will remove all hold tags from the specified snapshot.
        
        `options.recursive` will release snapshots recursively. Please note that only the tags that are present on the
        parent snapshot will be removed.

        Parameters
        ----------
        id:
            Release held snapshot `id`.
        options:
            options
        Returns
        -------
        """
        ...
    @typing.overload
    def remove(self, 
        snapshot_remove:'SnapshotRemove'={},
    /) -> None: 
        """
        Remove a snapshot from a given dataset.
        
        Returns:
            bool: True if succeed otherwise False.

        Parameters
        ----------
        snapshot_remove:
            snapshot_remove
        Returns
        -------
        """
        ...
    @typing.overload
    def rollback(self, 
        id:'str',
        options:'Options__'={},
    /) -> None: 
        """
        Rollback to a given snapshot `id`.
        
        `options.recursive` will destroy any snapshots and bookmarks more recent than the one
        specified.
        
        `options.recursive_clones` is just like `recursive` but will also destroy any clones.
        
        `options.force` will force unmount of any clones.
        
        `options.recursive_rollback` will do a complete recursive rollback of each child snapshots for `id`. If
        any child does not have specified snapshot, this operation will fail.

        Parameters
        ----------
        id:
            Rollback to a given snapshot `id`.
        options:
            options
        Returns
        -------
        """
        ...
    @typing.overload
    def update(self, 
        id:'str',
        snapshot_update:'SnapshotUpdate'={},
    /) -> 'dict[str]': 
        """
        

        Parameters
        ----------
        id:
            id
        snapshot_update:
            snapshot_update
        Returns
        -------
        dict[str]:
            zfs_snapshot_update_returns
        """
        ...

class SnapshotClone(typing.TypedDict):
        snapshot:'str'
        dataset_dst:'str'
        dataset_properties:'dict[str]'
        ...
class SnapshotCreate(typing.TypedDict):
        dataset:'str'
        name:'str'
        naming_schema:'str'
        recursive:'bool'
        exclude:'list[str]'
        suspend_vms:'bool'
        vmware_sync:'bool'
        properties:'dict[str]'
        ...
class Options(typing.TypedDict):
        defer:'bool'
        recursive:'bool'
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
class Options_(typing.TypedDict):
        recursive:'bool'
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
class SnapshotRemove(typing.TypedDict):
        dataset:'str'
        name:'str'
        defer_delete:'bool'
        ...
class Options__(typing.TypedDict):
        recursive:'bool'
        recursive_clones:'bool'
        force:'bool'
        recursive_rollback:'bool'
        ...
class SnapshotUpdate(typing.TypedDict):
        user_properties_update:'list[UserProperty]'
        ...
class UserProperty(typing.TypedDict):
        key:'str'
        value:'str'
        remove:'bool'
        ...