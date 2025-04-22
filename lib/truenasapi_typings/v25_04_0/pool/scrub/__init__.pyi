from pytruenas import Namespace as _NS 
class PoolScrub(_NS):
    
    def create(self,
        data,
    ) -> PoolScrubCreate:
        """Create a scrub task for a pool.

`threshold` refers to the minimum amount of time in days has to be passed before a scrub can run again."""
        ...
    def delete(self,
        id_,
    ) -> PoolScrubDelete:
        """Delete scrub task of `id`."""
        ...
    def get_instance(self,
        id,
        options,
    ) -> PoolScrubGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
    ) -> PoolScrubQuery:
        """"""
        ...
    def run(self,
        name,
        threshold,
    ) -> PoolScrubRun:
        """Initiate a scrub of a pool `name` if last scrub was performed more than `threshold` days before."""
        ...
    def scrub(self,
        name,
        action,
    ) -> PoolScrubScrub:
        """Start/Stop/Pause a scrub on pool `name`."""
        ...
    def update(self,
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