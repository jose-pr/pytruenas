
from pytruenas import Namespace
class Activedirectory(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'activedirectory')

