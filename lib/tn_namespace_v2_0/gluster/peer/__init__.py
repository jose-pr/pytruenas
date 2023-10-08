
from pytruenas import Namespace
class GlusterPeer(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'gluster.peer')

