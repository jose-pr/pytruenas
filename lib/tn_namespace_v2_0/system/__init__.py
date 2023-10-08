
from pytruenas import Namespace
class System(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'system')

