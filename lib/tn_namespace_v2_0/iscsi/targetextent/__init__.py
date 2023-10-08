
from pytruenas import Namespace
class IscsiTargetextent(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'iscsi.targetextent')

