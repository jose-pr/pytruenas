
from pytruenas import Namespace
class AcmeDnsAuthenticator(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'acme.dns.authenticator')

