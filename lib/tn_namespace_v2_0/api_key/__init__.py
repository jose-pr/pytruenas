
from pytruenas import Namespace
class Api_key(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'api_key')

