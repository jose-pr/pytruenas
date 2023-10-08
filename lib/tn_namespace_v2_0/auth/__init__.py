
from pytruenas import Namespace
class Auth(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'auth')

