
from pytruenas import Namespace
class App(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'app')

