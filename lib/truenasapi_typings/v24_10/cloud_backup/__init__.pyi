from pytruenas import Namespace as _NS
import typing as _ty 
class Cloud_backup(_NS):
    
    def abort(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Cloud_backupAbort:
        """Abort a running cloud backup task."""
        ...
    def create(self,
        cloud_backup,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Cloud_backupCreate:
        """Create a new cloud backup task"""
        ...
    def delete(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Cloud_backupDelete:
        """Delete cloud backup entry `id`."""
        ...
    def delete_snapshot(self,
        id,
        snapshot_id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Cloud_backupDelete_snapshot:
        """Delete snapshot `snapshot_id` created by the cloud backup job `id`."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Cloud_backupGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def list_snapshot_directory(self,
        id,
        snapshot_id,
        path,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Cloud_backupList_snapshot_directory:
        """List files in the directory `path` of the `snapshot_id` created by the cloud backup job `id`."""
        ...
    def list_snapshots(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Cloud_backupList_snapshots:
        """List existing snapshots for the cloud backup job `id`."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Cloud_backupQuery:
        """"""
        ...
    def restore(self,
        id,
        snapshot_id,
        subfolder,
        destination_path,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Cloud_backupRestore:
        """Restore files to the directory `destination_path` from the `snapshot_id` subfolder `subfolder` created by the cloud backup job `id`."""
        ...
    def sync(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Cloud_backupSync:
        """Run the cloud backup job `id`."""
        ...
    def transfer_setting_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Cloud_backupTransfer_setting_choices:
        """Return all possible choices for `cloud_backup.create.transfer_setting`."""
        ...
    def update(self,
        id,
        data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Cloud_backupUpdate:
        """Update the cloud backup entry `id` with `data`."""
        ...
class Cloud_backupAbort(_ty.TypedDict):
    ...
class Cloud_backupCreate(_ty.TypedDict):
    ...
class Cloud_backupDelete(_ty.TypedDict):
    ...
class Cloud_backupDelete_snapshot(_ty.TypedDict):
    ...
class Cloud_backupGet_instance(_ty.TypedDict):
    ...
class Cloud_backupList_snapshot_directory(_ty.TypedDict):
    ...
class Cloud_backupList_snapshots(_ty.TypedDict):
    ...
class Cloud_backupQuery(_ty.TypedDict):
    ...
class Cloud_backupRestore(_ty.TypedDict):
    ...
class Cloud_backupSync(_ty.TypedDict):
    ...
class Cloud_backupTransfer_setting_choices(_ty.TypedDict):
    ...
class Cloud_backupUpdate(_ty.TypedDict):
    ... 