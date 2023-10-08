
from pytruenas import Namespace
class IscsiInitiator(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'iscsi.initiator')

