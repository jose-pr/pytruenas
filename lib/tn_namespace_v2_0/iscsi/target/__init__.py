
from pytruenas import Namespace
class IscsiTarget(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'iscsi.target')

