from pytruenas import Namespace as _NS

from .dataset import PoolDataset

from .resilver import PoolResilver

from .scrub import PoolScrub

from .snapshottask import PoolSnapshottask
 
class Pool(_NS):
    
    def ddt_prefetch(
        
    ) -> PoolDdt_prefetch:
        ...
    
    def ddt_prune(
        
    ) -> PoolDdt_prune:
        ...
     
    
    dataset: PoolDataset
    
    resilver: PoolResilver
    
    scrub: PoolScrub
    
    snapshottask: PoolSnapshottask
     



class PoolDdt_prefetch:
    ...

class PoolDdt_prune:
    ...
 