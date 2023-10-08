
from pytruenas import Namespace
class AuthTwofactor(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'auth.twofactor')

