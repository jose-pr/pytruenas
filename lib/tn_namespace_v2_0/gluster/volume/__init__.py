
from pytruenas import Namespace
class GlusterVolume(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'gluster.volume')

