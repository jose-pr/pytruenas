
from pytruenas import Namespace
class IscsiExtent(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'iscsi.extent')

