
from pytruenas import Namespace
class Kerberos(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'kerberos')

