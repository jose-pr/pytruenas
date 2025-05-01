from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Snapshottask(_NS):
    
    def _create(self,
        **fields:_ty.Unpack[Data],
    ) -> CreateReturn:
        """"""
        ...
    def _get(self,
        __id_or_filter:int|_ty.Sequence[str]|None=None,
        **fields:_ty.Unpack[Get],
    ) -> GetInstanceReturn|None:
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
    def create(self,
        data:CreateData,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateReturn:
        """Create a Periodic Snapshot Task

Create a Periodic Snapshot Task that will take snapshots of specified `dataset` at specified `schedule`. Recursive snapshots can be created if `recursive` flag is enabled. You can `exclude` specific child datasets or zvols from the snapshot. Snapshots will be automatically destroyed after a certain amount of time, specified by `lifetime_value` and `lifetime_unit`. If multiple periodic tasks create snapshots at the same time (for example hourly and daily at 00:00) the snapshot will be kept until the last of these tasks reaches its expiry time. Snapshots will be named according to `naming_schema` which is a `strftime`-like template for snapshot name and must contain `%Y`, `%m`, `%d`, `%H` and `%M`."""
        ...
    def delete(self,
        id:int,
        options:DeleteOptions,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete a Periodic Snapshot Task with specific `id`"""
        ...
    def delete_will_change_retention_for(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Returns a list of snapshots which will change the retention if periodic snapshot task `id` is deleted."""
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
    def max_count(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> int:
        """Returns a maximum amount of snapshots (per-dataset) the system can sustain."""
        ...
    def max_total_count(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> int:
        """Returns a maximum amount of snapshots (total) the system can sustain."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:QueryOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[QueryPoolSnapshotTaskQueryResultItem]|QueryPoolSnapshotTaskQueryResultItem|int:
        """"""
        ...
    def run(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Execute a Periodic Snapshot Task of `id`."""
        ...
    def update(self,
        id:int,
        data:UpdateData,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update a Periodic Snapshot Task with specific `id`

See the documentation for `create` method for information on payload contents"""
        ...
    def update_will_change_retention_for(self,
        id:int,
        data:UpdateWillChangeRetentionForData,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Returns a list of snapshots which will change the retention if periodic snapshot task `id` is updated with `data`."""
        ...
Data = _ty.TypedDict('Data', {
    'dataset': _ty.NotRequired[str],
    'recursive': _ty.NotRequired[bool],
    'lifetime_value': _ty.NotRequired[int],
    'lifetime_unit': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'exclude': _ty.NotRequired[list[str]],
    'naming_schema': _ty.NotRequired[str],
    'allow_empty': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'fixate_removal_date': _ty.NotRequired[bool], 
})
Get = _ty.TypedDict('Get', {
    'dataset': _ty.NotRequired[str],
    'recursive': _ty.NotRequired[bool],
    'lifetime_value': _ty.NotRequired[int],
    'lifetime_unit': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'exclude': _ty.NotRequired[list[str]],
    'naming_schema': _ty.NotRequired[str],
    'allow_empty': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'id': _ty.NotRequired[int],
    'vmware_sync': _ty.NotRequired[bool],
    'state': _ty.NotRequired[_jsonschema.JsonValue], 
})
CreateData = _ty.TypedDict('CreateData', {
    'dataset': str,
    'recursive': _ty.NotRequired[bool],
    'lifetime_value': _ty.NotRequired[int],
    'lifetime_unit': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'exclude': _ty.NotRequired[list[str]],
    'naming_schema': _ty.NotRequired[str],
    'allow_empty': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue], 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'dataset': str,
    'recursive': _ty.NotRequired[bool],
    'lifetime_value': _ty.NotRequired[int],
    'lifetime_unit': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'exclude': _ty.NotRequired[list[str]],
    'naming_schema': _ty.NotRequired[str],
    'allow_empty': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'id': int,
    'vmware_sync': bool,
    'state': _jsonschema.JsonValue, 
})
DeleteOptions = _ty.TypedDict('DeleteOptions', {
    'fixate_removal_date': _ty.NotRequired[bool], 
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
    'dataset': str,
    'recursive': _ty.NotRequired[bool],
    'lifetime_value': _ty.NotRequired[int],
    'lifetime_unit': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'exclude': _ty.NotRequired[list[str]],
    'naming_schema': _ty.NotRequired[str],
    'allow_empty': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'id': int,
    'vmware_sync': bool,
    'state': _jsonschema.JsonValue, 
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
QueryPoolSnapshotTaskQueryResultItem = _ty.TypedDict('QueryPoolSnapshotTaskQueryResultItem', {
    'dataset': _ty.NotRequired[str],
    'recursive': _ty.NotRequired[bool],
    'lifetime_value': _ty.NotRequired[int],
    'lifetime_unit': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'exclude': _ty.NotRequired[list[str]],
    'naming_schema': _ty.NotRequired[str],
    'allow_empty': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'id': _ty.NotRequired[int],
    'vmware_sync': _ty.NotRequired[bool],
    'state': _ty.NotRequired[_jsonschema.JsonValue], 
})
UpdateData = _ty.TypedDict('UpdateData', {
    'dataset': _ty.NotRequired[str],
    'recursive': _ty.NotRequired[bool],
    'lifetime_value': _ty.NotRequired[int],
    'lifetime_unit': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'exclude': _ty.NotRequired[list[str]],
    'naming_schema': _ty.NotRequired[str],
    'allow_empty': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'fixate_removal_date': _ty.NotRequired[bool], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'dataset': str,
    'recursive': _ty.NotRequired[bool],
    'lifetime_value': _ty.NotRequired[int],
    'lifetime_unit': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'exclude': _ty.NotRequired[list[str]],
    'naming_schema': _ty.NotRequired[str],
    'allow_empty': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'id': int,
    'vmware_sync': bool,
    'state': _jsonschema.JsonValue, 
})
UpdateWillChangeRetentionForData = _ty.TypedDict('UpdateWillChangeRetentionForData', {
    'dataset': _ty.NotRequired[str],
    'recursive': _ty.NotRequired[bool],
    'lifetime_value': _ty.NotRequired[int],
    'lifetime_unit': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'exclude': _ty.NotRequired[list[str]],
    'naming_schema': _ty.NotRequired[str],
    'allow_empty': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue], 
})