from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .dataset import PoolDataset
from .resilver import PoolResilver
from .scrub import PoolScrub
from .snapshottask import PoolSnapshottask 
class Pool(_NS):
    
    def ddt_prefetch(self,
        pool_name:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Prefetch DDT entries in pool `pool_name`."""
        ...
    def ddt_prune(self,
        options:options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Prune DDT entries in pool `pool_name` based on the specified options.

`percentage` is the percentage of DDT entries to prune.

`days` is the number of days to prune DDT entries."""
        ...
    dataset: PoolDataset
    resilver: PoolResilver
    scrub: PoolScrub
    snapshottask: PoolSnapshottask
options = _ty.TypedDict('options', {
    'pool_name': str,
    'percentage': _ty.NotRequired[int|None],
    'days': _ty.NotRequired[int|None], 
})