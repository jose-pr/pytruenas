from pytruenas import Namespace as _NS
import typing as _ty
from .dataset import PoolDataset
from .resilver import PoolResilver
from .scrub import PoolScrub
from .snapshottask import PoolSnapshottask 
class Pool(_NS):
    
    def ddt_prefetch(self,
        pool_name,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolDdt_prefetch:
        """Prefetch DDT entries in pool `pool_name`."""
        ...
    def ddt_prune(self,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolDdt_prune:
        """Prune DDT entries in pool `pool_name` based on the specified options.

`percentage` is the percentage of DDT entries to prune.

`days` is the number of days to prune DDT entries."""
        ...
    dataset: PoolDataset
    resilver: PoolResilver
    scrub: PoolScrub
    snapshottask: PoolSnapshottask
class PoolDdt_prefetch(_ty.TypedDict):
    ...
class PoolDdt_prune(_ty.TypedDict):
    ... 