
from pytruenas import Namespace
class SystemAdvanced(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'system.advanced')

