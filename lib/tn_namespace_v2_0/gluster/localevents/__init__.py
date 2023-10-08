
from pytruenas import Namespace
class GlusterLocalevents(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'gluster.localevents')

