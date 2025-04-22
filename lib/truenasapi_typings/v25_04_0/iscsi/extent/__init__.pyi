from pytruenas import Namespace as _NS 
class IscsiExtent(_NS):
    
    def create(self,
        iscsi_extent_create,
    ) -> IscsiExtentCreate:
        """Create an iSCSI Extent.

When `type` is set to FILE, attribute `filesize` is used and it represents number of bytes. `filesize` if not zero should be a multiple of `blocksize`. `path` is a required attribute with `type` set as FILE.

With `type` being set to DISK, a valid ZFS volume is required.

`insecure_tpc` when enabled allows an initiator to bypass normal access control and access any scannable target. This allows xcopy operations otherwise blocked by access control.

`xen` is a boolean value which is set to true if Xen is being used as the iSCSI initiator.

`ro` when set to true prevents the initiator from writing to this LUN."""
        ...
    def delete(self,
        id,
        remove,
        force,
    ) -> IscsiExtentDelete:
        """Delete iSCSI Extent of `id`.

If `id` iSCSI Extent's `type` was configured to FILE, `remove` can be set to remove the configured file."""
        ...
    def disk_choices(self,
    ) -> IscsiExtentDisk_choices:
        """Return a dict of available zvols that can be used when creating an extent."""
        ...
    def get_instance(self,
        id,
        options,
    ) -> IscsiExtentGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
    ) -> IscsiExtentQuery:
        """"""
        ...
    def update(self,
        id,
        iscsi_extent_update,
    ) -> IscsiExtentUpdate:
        """Update iSCSI Extent of `id`."""
        ...
class IscsiExtentCreate:
    ...
class IscsiExtentDelete:
    ...
class IscsiExtentDisk_choices:
    ...
class IscsiExtentGet_instance:
    ...
class IscsiExtentQuery:
    ...
class IscsiExtentUpdate:
    ... 