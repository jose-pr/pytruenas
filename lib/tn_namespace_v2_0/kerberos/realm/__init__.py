
from pytruenas import Namespace
class KerberosRealm(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'kerberos.realm')

