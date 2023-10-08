
from pytruenas import Namespace
class SystemNtpserver(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'system.ntpserver')

