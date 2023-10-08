
from pytruenas import Namespace
class Cloud_backup(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'cloud_backup')

