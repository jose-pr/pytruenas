
from pytruenas import Namespace
class Update(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'update')

