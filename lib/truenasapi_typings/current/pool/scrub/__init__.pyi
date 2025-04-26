from pytruenas import Namespace as _NS
import typing as _ty 
class PoolScrub(_NS):
    
    def create(self,
        data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolScrubCreate:
        """Create a scrub task for a pool.

`threshold` refers to the minimum amount of time in days has to be passed before a scrub can run again."""
        ...
    def delete(self,
        id_,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolScrubDelete:
        """Delete scrub task of `id`."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolScrubGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolScrubQuery:
        """"""
        ...
    def run(self,
        name,
        threshold,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolScrubRun:
        """Initiate a scrub of a pool `name` if last scrub was performed more than `threshold` days before."""
        ...
    def scrub(self,
        name,
        action,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolScrubScrub:
        """Start/Stop/Pause a scrub on pool `name`."""
        ...
    def update(self,
        id_,
        data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolScrubUpdate:
        """Update scrub task of `id`."""
        ...
class PoolScrubCreate(_ty.TypedDict):
    ...
class PoolScrubDelete(_ty.TypedDict):
    ...
class PoolScrubGet_instance(_ty.TypedDict):
    ...
class PoolScrubQuery(_ty.TypedDict):
    ...
class PoolScrubRun(_ty.TypedDict):
    ...
class PoolScrubScrub(_ty.TypedDict):
    ...
class PoolScrubUpdate(_ty.TypedDict):
    ... 