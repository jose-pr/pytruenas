
from pytruenas import Namespace
class GlusterEventsd(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'gluster.eventsd')

