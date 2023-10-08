
from pytruenas import Namespace
class CtdbPublicIps(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ctdb.public.ips')

