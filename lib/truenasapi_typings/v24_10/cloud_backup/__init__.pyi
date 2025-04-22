from pytruenas import Namespace as _NS 
class Cloud_backup(_NS):
    
    def abort(self,
        id,
    ) -> Cloud_backupAbort:
        """Abort a running cloud backup task."""
        ...
    def create(self,
        cloud_backup,
    ) -> Cloud_backupCreate:
        """Create a new cloud backup task"""
        ...
    def delete(self,
        id,
    ) -> Cloud_backupDelete:
        """Delete cloud backup entry `id`."""
        ...
    def delete_snapshot(self,
        id,
        snapshot_id,
    ) -> Cloud_backupDelete_snapshot:
        """Delete snapshot `snapshot_id` created by the cloud backup job `id`."""
        ...
    def get_instance(self,
        id,
        options,
    ) -> Cloud_backupGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def list_snapshot_directory(self,
        id,
        snapshot_id,
        path,
    ) -> Cloud_backupList_snapshot_directory:
        """List files in the directory `path` of the `snapshot_id` created by the cloud backup job `id`."""
        ...
    def list_snapshots(self,
        id,
    ) -> Cloud_backupList_snapshots:
        """List existing snapshots for the cloud backup job `id`."""
        ...
    def query(self,
        filters,
        options,
    ) -> Cloud_backupQuery:
        """"""
        ...
    def restore(self,
        id,
        snapshot_id,
        subfolder,
        destination_path,
        options,
    ) -> Cloud_backupRestore:
        """Restore files to the directory `destination_path` from the `snapshot_id` subfolder `subfolder` created by the cloud backup job `id`."""
        ...
    def sync(self,
        id,
        options,
    ) -> Cloud_backupSync:
        """Run the cloud backup job `id`."""
        ...
    def transfer_setting_choices(self,
    ) -> Cloud_backupTransfer_setting_choices:
        """Return all possible choices for `cloud_backup.create.transfer_setting`."""
        ...
    def update(self,
        id,
        data,
    ) -> Cloud_backupUpdate:
        """Update the cloud backup entry `id` with `data`."""
        ...
class Cloud_backupAbort:
    ...
class Cloud_backupCreate:
    ...
class Cloud_backupDelete:
    ...
class Cloud_backupDelete_snapshot:
    ...
class Cloud_backupGet_instance:
    ...
class Cloud_backupList_snapshot_directory:
    ...
class Cloud_backupList_snapshots:
    ...
class Cloud_backupQuery:
    ...
class Cloud_backupRestore:
    ...
class Cloud_backupSync:
    ...
class Cloud_backupTransfer_setting_choices:
    ...
class Cloud_backupUpdate:
    ... 