
from pytruenas import Namespace
class IscsiPortal(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'iscsi.portal')
