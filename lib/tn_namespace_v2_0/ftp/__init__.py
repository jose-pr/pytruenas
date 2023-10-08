
from pytruenas import Namespace
class Ftp(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ftp')

