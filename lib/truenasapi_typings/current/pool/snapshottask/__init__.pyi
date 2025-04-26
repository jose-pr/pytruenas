from pytruenas import Namespace as _NS
import typing as _ty 
class PoolSnapshottask(_NS):
    
    def create(self,
        data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolSnapshottaskCreate:
        """Create a Periodic Snapshot Task

Create a Periodic Snapshot Task that will take snapshots of specified `dataset` at specified `schedule`. Recursive snapshots can be created if `recursive` flag is enabled. You can `exclude` specific child datasets or zvols from the snapshot. Snapshots will be automatically destroyed after a certain amount of time, specified by `lifetime_value` and `lifetime_unit`. If multiple periodic tasks create snapshots at the same time (for example hourly and daily at 00:00) the snapshot will be kept until the last of these tasks reaches its expiry time. Snapshots will be named according to `naming_schema` which is a `strftime`-like template for snapshot name and must contain `%Y`, `%m`, `%d`, `%H` and `%M`."""
        ...
    def delete(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolSnapshottaskDelete:
        """Delete a Periodic Snapshot Task with specific `id`"""
        ...
    def delete_will_change_retention_for(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolSnapshottaskDelete_will_change_retention_for:
        """Returns a list of snapshots which will change the retention if periodic snapshot task `id` is deleted."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolSnapshottaskGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def max_count(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolSnapshottaskMax_count:
        """Returns a maximum amount of snapshots (per-dataset) the system can sustain."""
        ...
    def max_total_count(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolSnapshottaskMax_total_count:
        """Returns a maximum amount of snapshots (total) the system can sustain."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolSnapshottaskQuery:
        """"""
        ...
    def run(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolSnapshottaskRun:
        """Execute a Periodic Snapshot Task of `id`."""
        ...
    def update(self,
        id,
        data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolSnapshottaskUpdate:
        """Update a Periodic Snapshot Task with specific `id`

See the documentation for `create` method for information on payload contents"""
        ...
    def update_will_change_retention_for(self,
        id,
        data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolSnapshottaskUpdate_will_change_retention_for:
        """Returns a list of snapshots which will change the retention if periodic snapshot task `id` is updated with `data`."""
        ...
class PoolSnapshottaskCreate(_ty.TypedDict):
    ...
class PoolSnapshottaskDelete(_ty.TypedDict):
    ...
class PoolSnapshottaskDelete_will_change_retention_for(_ty.TypedDict):
    ...
class PoolSnapshottaskGet_instance(_ty.TypedDict):
    ...
class PoolSnapshottaskMax_count(_ty.TypedDict):
    ...
class PoolSnapshottaskMax_total_count(_ty.TypedDict):
    ...
class PoolSnapshottaskQuery(_ty.TypedDict):
    ...
class PoolSnapshottaskRun(_ty.TypedDict):
    ...
class PoolSnapshottaskUpdate(_ty.TypedDict):
    ...
class PoolSnapshottaskUpdate_will_change_retention_for(_ty.TypedDict):
    ... 