
from pytruenas import Namespace
class Systemdataset(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'systemdataset')

