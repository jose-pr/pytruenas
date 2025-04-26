from pytruenas import Namespace as _NS
import typing as _ty 
class Cronjob(_NS):
    
    def create(self,
        data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CronjobCreate:
        """Create a new cron job.

`stderr` and `stdout` are boolean values which if `true`, represent that we would like to suppress standard error / standard output respectively."""
        ...
    def delete(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CronjobDelete:
        """Delete cronjob of `id`."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CronjobGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CronjobQuery:
        """"""
        ...
    def run(self,
        id,
        skip_disabled,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CronjobRun:
        """Job to run cronjob task of `id`."""
        ...
    def update(self,
        id,
        data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CronjobUpdate:
        """Update cronjob of `id`."""
        ...
class CronjobCreate(_ty.TypedDict):
    ...
class CronjobDelete(_ty.TypedDict):
    ...
class CronjobGet_instance(_ty.TypedDict):
    ...
class CronjobQuery(_ty.TypedDict):
    ...
class CronjobRun(_ty.TypedDict):
    ...
class CronjobUpdate(_ty.TypedDict):
    ... 