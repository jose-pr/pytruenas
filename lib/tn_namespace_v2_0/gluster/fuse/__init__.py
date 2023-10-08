
from pytruenas import Namespace
class GlusterFuse(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'gluster.fuse')

