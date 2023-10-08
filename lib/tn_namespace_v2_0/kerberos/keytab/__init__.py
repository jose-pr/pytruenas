
from pytruenas import Namespace
class KerberosKeytab(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'kerberos.keytab')

