
from pytruenas import Namespace
class Alertclasses(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'alertclasses')

