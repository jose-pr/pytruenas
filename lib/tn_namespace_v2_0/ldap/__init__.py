
from pytruenas import Namespace
class Ldap(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ldap')

