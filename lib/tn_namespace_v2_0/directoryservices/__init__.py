
from pytruenas import Namespace
class Directoryservices(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'directoryservices')

