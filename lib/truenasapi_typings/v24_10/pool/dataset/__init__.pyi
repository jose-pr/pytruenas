from pytruenas import Namespace as _NS
import typing as _ty 
class PoolDataset(_NS):
    
    def details(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolDatasetDetails:
        """Retrieve all dataset(s) details outlining any services/tasks which might be consuming them."""
        ...
    def snapshot_count(self,
        dataset,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolDatasetSnapshot_count:
        """Returns snapshot count for specified `dataset`."""
        ...
class PoolDatasetDetails(_ty.TypedDict):
    ...
class PoolDatasetSnapshot_count(_ty.TypedDict):
    ... 