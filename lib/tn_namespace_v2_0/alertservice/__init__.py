
from pytruenas import Namespace
class Alertservice(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'alertservice')

