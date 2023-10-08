
from pytruenas import Namespace
class SharingSmb(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'sharing.smb')

