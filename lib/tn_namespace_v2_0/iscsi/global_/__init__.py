
from pytruenas import Namespace
class IscsiGlobal_(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'iscsi.global')

