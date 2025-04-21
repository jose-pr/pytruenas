from pytruenas import Namespace as _NS
from .dataset import PoolDataset
from .resilver import PoolResilver
from .scrub import PoolScrub
from .snapshottask import PoolSnapshottask 
class Pool(_NS):
    
    def ddt_prefetch(
        pool_name,
    ) -> PoolDdt_prefetch:
        """Prefetch DDT entries in pool `pool_name`."""
        ...
    def ddt_prune(
        options,
    ) -> PoolDdt_prune:
        """Prune DDT entries in pool `pool_name` based on the specified options.

`percentage` is the percentage of DDT entries to prune.

`days` is the number of days to prune DDT entries."""
        ...
    dataset: PoolDataset
    resilver: PoolResilver
    scrub: PoolScrub
    snapshottask: PoolSnapshottask
class PoolDdt_prefetch:
    ...
class PoolDdt_prune:
    ... 