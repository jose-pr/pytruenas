
from pytruenas import Namespace
class CtdbPrivateIps(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ctdb.private.ips')

