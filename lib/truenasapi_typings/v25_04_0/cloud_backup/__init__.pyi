from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Cloud_backup(_NS):
    
    def abort(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Abort a running cloud backup task."""
        ...
    def create(self,
        cloud_backup:cloud_backup,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Cloud_backupCreate:
        """Create a new cloud backup task"""
        ...
    def delete(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete cloud backup entry `id`."""
        ...
    def delete_snapshot(self,
        id:int,
        snapshot_id:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Delete snapshot `snapshot_id` created by the cloud backup job `id`."""
        ...
    def get_instance(self,
        id:int,
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Cloud_backupGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def list_snapshot_directory(self,
        id:int,
        snapshot_id:str,
        path:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[CloudBackupSnapshotItem]:
        """List files in the directory `path` of the `snapshot_id` created by the cloud backup job `id`."""
        ...
    def list_snapshots(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[CloudBackupSnapshot]:
        """List existing snapshots for the cloud backup job `id`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[CloudBackupQueryResultItem]|CloudBackupQueryResultItem|int:
        """"""
        ...
    def restore(self,
        id:int,
        snapshot_id:str,
        subfolder:str,
        destination_path:str,
        options:options={'exclude': [], 'include': []},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Restore files to the directory `destination_path` from the `snapshot_id` subfolder `subfolder` created by the cloud backup job `id`."""
        ...
    def sync(self,
        id:int,
        options:options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Run the cloud backup job `id`."""
        ...
    def transfer_setting_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[str]:
        """Return all possible choices for `cloud_backup.create.transfer_setting`."""
        ...
    def update(self,
        id:int,
        data:data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Cloud_backupUpdate:
        """Update the cloud backup entry `id` with `data`."""
        ...
cloud_backup = _ty.TypedDict('cloud_backup', {
    'description': _ty.NotRequired[str],
    'path': str,
    'credentials': int,
    'attributes': _jsonschema.JsonObject,
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'pre_script': _ty.NotRequired[str],
    'post_script': _ty.NotRequired[str],
    'snapshot': _ty.NotRequired[bool],
    'include': _ty.NotRequired[list[str]],
    'exclude': _ty.NotRequired[list[str]],
    'args': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'password': str,
    'keep_last': int,
    'transfer_setting': _ty.NotRequired[str],
    'absolute_paths': _ty.NotRequired[bool], 
})
Cloud_backupCreate = _ty.TypedDict('Cloud_backupCreate', {
    'description': _ty.NotRequired[str],
    'path': str,
    'credentials': _jsonschema.JsonValue,
    'attributes': _jsonschema.JsonObject,
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'pre_script': _ty.NotRequired[str],
    'post_script': _ty.NotRequired[str],
    'snapshot': _ty.NotRequired[bool],
    'include': _ty.NotRequired[list[str]],
    'exclude': _ty.NotRequired[list[str]],
    'args': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'password': str,
    'keep_last': int,
    'transfer_setting': _ty.NotRequired[str],
    'absolute_paths': _ty.NotRequired[bool],
    'id': int,
    'job': _jsonschema.JsonObject|None,
    'locked': bool, 
})
options = _ty.TypedDict('options', {
    'dry_run': _ty.NotRequired[bool], 
})
Cloud_backupGet_instance = _ty.TypedDict('Cloud_backupGet_instance', {
    'description': _ty.NotRequired[str],
    'path': str,
    'credentials': _jsonschema.JsonValue,
    'attributes': _jsonschema.JsonObject,
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'pre_script': _ty.NotRequired[str],
    'post_script': _ty.NotRequired[str],
    'snapshot': _ty.NotRequired[bool],
    'include': _ty.NotRequired[list[str]],
    'exclude': _ty.NotRequired[list[str]],
    'args': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'password': str,
    'keep_last': int,
    'transfer_setting': _ty.NotRequired[str],
    'absolute_paths': _ty.NotRequired[bool],
    'id': int,
    'job': _jsonschema.JsonObject|None,
    'locked': bool, 
})
CloudBackupSnapshotItem = _ty.TypedDict('CloudBackupSnapshotItem', {
    'name': str,
    'path': str,
    'type': str,
    'size': int|None,
    'mtime': str, 
})
CloudBackupSnapshot = _ty.TypedDict('CloudBackupSnapshot', {
    'id': str,
    'hostname': str,
    'time': str,
    'paths': list[str], 
})
CloudBackupQueryResultItem = _ty.TypedDict('CloudBackupQueryResultItem', {
    'description': _ty.NotRequired[str],
    'path': _ty.NotRequired[str],
    'credentials': _ty.NotRequired[_jsonschema.JsonValue],
    'attributes': _ty.NotRequired[_jsonschema.JsonObject],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'pre_script': _ty.NotRequired[str],
    'post_script': _ty.NotRequired[str],
    'snapshot': _ty.NotRequired[bool],
    'include': _ty.NotRequired[list[str]],
    'exclude': _ty.NotRequired[list[str]],
    'args': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'password': _ty.NotRequired[str],
    'keep_last': _ty.NotRequired[int],
    'transfer_setting': _ty.NotRequired[str],
    'absolute_paths': _ty.NotRequired[bool],
    'id': _ty.NotRequired[int],
    'job': _ty.NotRequired[_jsonschema.JsonObject|None],
    'locked': _ty.NotRequired[bool], 
})
data = _ty.TypedDict('data', {
    'description': _ty.NotRequired[str],
    'path': _ty.NotRequired[str],
    'credentials': _ty.NotRequired[int],
    'attributes': _ty.NotRequired[_jsonschema.JsonObject],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'pre_script': _ty.NotRequired[str],
    'post_script': _ty.NotRequired[str],
    'snapshot': _ty.NotRequired[bool],
    'include': _ty.NotRequired[list[str]],
    'exclude': _ty.NotRequired[list[str]],
    'args': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'password': _ty.NotRequired[str],
    'keep_last': _ty.NotRequired[int],
    'transfer_setting': _ty.NotRequired[str], 
})
Cloud_backupUpdate = _ty.TypedDict('Cloud_backupUpdate', {
    'description': _ty.NotRequired[str],
    'path': str,
    'credentials': _jsonschema.JsonValue,
    'attributes': _jsonschema.JsonObject,
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'pre_script': _ty.NotRequired[str],
    'post_script': _ty.NotRequired[str],
    'snapshot': _ty.NotRequired[bool],
    'include': _ty.NotRequired[list[str]],
    'exclude': _ty.NotRequired[list[str]],
    'args': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'password': str,
    'keep_last': int,
    'transfer_setting': _ty.NotRequired[str],
    'absolute_paths': _ty.NotRequired[bool],
    'id': int,
    'job': _jsonschema.JsonObject|None,
    'locked': bool, 
})