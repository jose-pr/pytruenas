
from pytruenas import Namespace
class CtdbGeneral(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ctdb.general')

