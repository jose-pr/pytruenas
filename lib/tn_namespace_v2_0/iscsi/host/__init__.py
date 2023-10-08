
from pytruenas import Namespace
class IscsiHost(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'iscsi.host')

