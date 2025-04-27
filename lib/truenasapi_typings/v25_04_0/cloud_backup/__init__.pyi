from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class CloudBackup(_NS):
    
    def _create(self,
        **fields:_ty.Unpack[CloudBackup],
    ) -> CreateReturn:
        """"""
        ...
    def _update(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[Data],
    ) -> UpdateReturn:
        """"""
        ...
    def _upsert(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[Data],
    ) -> UpdateReturn:
        """"""
        ...
    def abort(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Abort a running cloud backup task."""
        ...
    def create(self,
        cloud_backup:CreateCloudBackup,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateReturn:
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
        options:GetInstanceOptions={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GetInstanceReturn:
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
    ) -> list[ListSnapshotDirectoryCloudBackupSnapshotItem]:
        """List files in the directory `path` of the `snapshot_id` created by the cloud backup job `id`."""
        ...
    def list_snapshots(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[ListSnapshotsCloudBackupSnapshot]:
        """List existing snapshots for the cloud backup job `id`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:QueryOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[QueryCloudBackupQueryResultItem]|QueryCloudBackupQueryResultItem|int:
        """"""
        ...
    def restore(self,
        id:int,
        snapshot_id:str,
        subfolder:str,
        destination_path:str,
        options:RestoreOptions={'exclude': [], 'include': []},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Restore files to the directory `destination_path` from the `snapshot_id` subfolder `subfolder` created by the cloud backup job `id`."""
        ...
    def sync(self,
        id:int,
        options:SyncOptions,
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
        data:UpdateData,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update the cloud backup entry `id` with `data`."""
        ...
CloudBackup = _ty.TypedDict('CloudBackup', {
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
Data = _ty.TypedDict('Data', {
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
CreateCloudBackup = _ty.TypedDict('CreateCloudBackup', {
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
CreateReturn = _ty.TypedDict('CreateReturn', {
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
GetInstanceOptions = _ty.TypedDict('GetInstanceOptions', {
    'relationships': _ty.NotRequired[bool],
    'extend': _ty.NotRequired[str|None],
    'extend_context': _ty.NotRequired[str|None],
    'prefix': _ty.NotRequired[str|None],
    'extra': _ty.NotRequired[_jsonschema.JsonObject],
    'order_by': _ty.NotRequired[list[str]],
    'select': _ty.NotRequired[list[str|_jsonschema.JsonArray]],
    'count': _ty.NotRequired[bool],
    'get': _ty.NotRequired[bool],
    'offset': _ty.NotRequired[int],
    'limit': _ty.NotRequired[int],
    'force_sql_filters': _ty.NotRequired[bool], 
})
GetInstanceReturn = _ty.TypedDict('GetInstanceReturn', {
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
ListSnapshotDirectoryCloudBackupSnapshotItem = _ty.TypedDict('ListSnapshotDirectoryCloudBackupSnapshotItem', {
    'name': str,
    'path': str,
    'type': str,
    'size': int|None,
    'mtime': str, 
})
ListSnapshotsCloudBackupSnapshot = _ty.TypedDict('ListSnapshotsCloudBackupSnapshot', {
    'id': str,
    'hostname': str,
    'time': str,
    'paths': list[str], 
})
QueryOptions = _ty.TypedDict('QueryOptions', {
    'relationships': _ty.NotRequired[bool],
    'extend': _ty.NotRequired[str|None],
    'extend_context': _ty.NotRequired[str|None],
    'prefix': _ty.NotRequired[str|None],
    'extra': _ty.NotRequired[_jsonschema.JsonObject],
    'order_by': _ty.NotRequired[list[str]],
    'select': _ty.NotRequired[list[str|_jsonschema.JsonArray]],
    'count': _ty.NotRequired[bool],
    'get': _ty.NotRequired[bool],
    'offset': _ty.NotRequired[int],
    'limit': _ty.NotRequired[int],
    'force_sql_filters': _ty.NotRequired[bool], 
})
QueryCloudBackupQueryResultItem = _ty.TypedDict('QueryCloudBackupQueryResultItem', {
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
RestoreOptions = _ty.TypedDict('RestoreOptions', {
    'exclude': _ty.NotRequired[list[str]],
    'include': _ty.NotRequired[list[str]], 
})
SyncOptions = _ty.TypedDict('SyncOptions', {
    'dry_run': _ty.NotRequired[bool], 
})
UpdateData = _ty.TypedDict('UpdateData', {
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
UpdateReturn = _ty.TypedDict('UpdateReturn', {
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