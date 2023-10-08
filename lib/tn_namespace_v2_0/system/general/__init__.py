
from pytruenas import Namespace
class SystemGeneral(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'system.general')

