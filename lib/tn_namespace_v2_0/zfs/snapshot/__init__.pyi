
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class ZfsSnapshot(Namespace):
    _namespace:_ty.Literal['zfs.snapshot']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def clone(self, 
        snapshot_clone:'dict[str]'={},
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
    @_ty.overload
    def create(self, 
        snapshot_create:'dict[str]'={},
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
    @_ty.overload
    def delete(self, 
        id:'str',
        options:'dict[str]'={},
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
    def hold(self, 
        id:'str',
        options:'dict[str]'={},
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
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
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
        list:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @_ty.overload
    def release(self, 
        id:'str',
        options:'dict[str]'={},
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
    @_ty.overload
    def remove(self, 
        snapshot_remove:'dict[str]'={},
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
    @_ty.overload
    def rollback(self, 
        id:'str',
        options:'dict[str]'={},
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
    @_ty.overload
    def update(self, 
        id:'str',
        snapshot_update:'dict[str]'={},
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
