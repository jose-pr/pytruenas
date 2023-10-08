
from pytruenas import Namespace
class Reporting(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'reporting')

