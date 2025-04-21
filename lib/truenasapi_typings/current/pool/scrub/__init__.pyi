from pytruenas import Namespace as _NS 
class PoolScrub(_NS):
    
    def create(
        data,
    ) -> PoolScrubCreate:
        """Create a scrub task for a pool.

`threshold` refers to the minimum amount of time in days has to be passed before a scrub can run again."""
        ...
    def delete(
        id_,
    ) -> PoolScrubDelete:
        """Delete scrub task of `id`."""
        ...
    def get_instance(
        id,
        options,
    ) -> PoolScrubGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(
        filters,
        options,
    ) -> PoolScrubQuery:
        """"""
        ...
    def run(
        name,
        threshold,
    ) -> PoolScrubRun:
        """Initiate a scrub of a pool `name` if last scrub was performed more than `threshold` days before."""
        ...
    def scrub(
        name,
        action,
    ) -> PoolScrubScrub:
        """Start/Stop/Pause a scrub on pool `name`."""
        ...
    def update(
        id_,
        data,
    ) -> PoolScrubUpdate:
        """Update scrub task of `id`."""
        ...
class PoolScrubCreate:
    ...
class PoolScrubDelete:
    ...
class PoolScrubGet_instance:
    ...
class PoolScrubQuery:
    ...
class PoolScrubRun:
    ...
class PoolScrubScrub:
    ...
class PoolScrubUpdate:
    ... 