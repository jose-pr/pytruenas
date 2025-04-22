from pytruenas import Namespace as _NS 
class Cronjob(_NS):
    
    def create(self,
        data,
    ) -> CronjobCreate:
        """Create a new cron job.

`stderr` and `stdout` are boolean values which if `true`, represent that we would like to suppress standard error / standard output respectively."""
        ...
    def delete(self,
        id,
    ) -> CronjobDelete:
        """Delete cronjob of `id`."""
        ...
    def get_instance(self,
        id,
        options,
    ) -> CronjobGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
    ) -> CronjobQuery:
        """"""
        ...
    def run(self,
        id,
        skip_disabled,
    ) -> CronjobRun:
        """Job to run cronjob task of `id`."""
        ...
    def update(self,
        id,
        data,
    ) -> CronjobUpdate:
        """Update cronjob of `id`."""
        ...
class CronjobCreate:
    ...
class CronjobDelete:
    ...
class CronjobGet_instance:
    ...
class CronjobQuery:
    ...
class CronjobRun:
    ...
class CronjobUpdate:
    ... 