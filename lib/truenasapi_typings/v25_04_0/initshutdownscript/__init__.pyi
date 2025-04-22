from pytruenas import Namespace as _NS 
class Initshutdownscript(_NS):
    
    def create(self,
        data,
    ) -> InitshutdownscriptCreate:
        """Create an initshutdown script task.

`type` indicates if a command or script should be executed at `when`.

There are three choices for `when`:

1) PREINIT - This is early in the boot process before all the services have started 2) POSTINIT - This is late in the boot process when most of the services have started 3) SHUTDOWN - This is on shutdown

`timeout` is an integer value which indicates time in seconds which the system should wait for the execution of script/command. It should be noted that a hard limit for a timeout is configured by the base OS, so when a script/command is set to execute on SHUTDOWN, the hard limit configured by the base OS is changed adding the timeout specified by script/command so it can be ensured that it executes as desired and is not interrupted by the base OS's limit."""
        ...
    def delete(self,
        id,
    ) -> InitshutdownscriptDelete:
        """Delete init/shutdown task of `id`."""
        ...
    def get_instance(self,
        id,
        options,
    ) -> InitshutdownscriptGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
    ) -> InitshutdownscriptQuery:
        """"""
        ...
    def update(self,
        id,
        data,
    ) -> InitshutdownscriptUpdate:
        """Update initshutdown script task of `id`."""
        ...
class InitshutdownscriptCreate:
    ...
class InitshutdownscriptDelete:
    ...
class InitshutdownscriptGet_instance:
    ...
class InitshutdownscriptQuery:
    ...
class InitshutdownscriptUpdate:
    ... 