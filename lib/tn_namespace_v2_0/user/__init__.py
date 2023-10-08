
from pytruenas import Namespace
class User(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'user')

