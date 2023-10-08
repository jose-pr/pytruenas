
from pytruenas import Namespace
class CloudsyncCredentials(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'cloudsync.credentials')

