from pytruenas import Namespace as _NS 
class PoolSnapshottask(_NS):
    
    def create(self,
        data,
    ) -> PoolSnapshottaskCreate:
        """Create a Periodic Snapshot Task

Create a Periodic Snapshot Task that will take snapshots of specified `dataset` at specified `schedule`. Recursive snapshots can be created if `recursive` flag is enabled. You can `exclude` specific child datasets or zvols from the snapshot. Snapshots will be automatically destroyed after a certain amount of time, specified by `lifetime_value` and `lifetime_unit`. If multiple periodic tasks create snapshots at the same time (for example hourly and daily at 00:00) the snapshot will be kept until the last of these tasks reaches its expiry time. Snapshots will be named according to `naming_schema` which is a `strftime`-like template for snapshot name and must contain `%Y`, `%m`, `%d`, `%H` and `%M`."""
        ...
    def delete(self,
        id,
        options,
    ) -> PoolSnapshottaskDelete:
        """Delete a Periodic Snapshot Task with specific `id`"""
        ...
    def delete_will_change_retention_for(self,
        id,
    ) -> PoolSnapshottaskDelete_will_change_retention_for:
        """Returns a list of snapshots which will change the retention if periodic snapshot task `id` is deleted."""
        ...
    def get_instance(self,
        id,
        options,
    ) -> PoolSnapshottaskGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def max_count(self,
    ) -> PoolSnapshottaskMax_count:
        """Returns a maximum amount of snapshots (per-dataset) the system can sustain."""
        ...
    def max_total_count(self,
    ) -> PoolSnapshottaskMax_total_count:
        """Returns a maximum amount of snapshots (total) the system can sustain."""
        ...
    def query(self,
        filters,
        options,
    ) -> PoolSnapshottaskQuery:
        """"""
        ...
    def run(self,
        id,
    ) -> PoolSnapshottaskRun:
        """Execute a Periodic Snapshot Task of `id`."""
        ...
    def update(self,
        id,
        data,
    ) -> PoolSnapshottaskUpdate:
        """Update a Periodic Snapshot Task with specific `id`

See the documentation for `create` method for information on payload contents"""
        ...
    def update_will_change_retention_for(self,
        id,
        data,
    ) -> PoolSnapshottaskUpdate_will_change_retention_for:
        """Returns a list of snapshots which will change the retention if periodic snapshot task `id` is updated with `data`."""
        ...
class PoolSnapshottaskCreate:
    ...
class PoolSnapshottaskDelete:
    ...
class PoolSnapshottaskDelete_will_change_retention_for:
    ...
class PoolSnapshottaskGet_instance:
    ...
class PoolSnapshottaskMax_count:
    ...
class PoolSnapshottaskMax_total_count:
    ...
class PoolSnapshottaskQuery:
    ...
class PoolSnapshottaskRun:
    ...
class PoolSnapshottaskUpdate:
    ...
class PoolSnapshottaskUpdate_will_change_retention_for:
    ... 