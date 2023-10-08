
from pytruenas import Namespace
class Support(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'support')

