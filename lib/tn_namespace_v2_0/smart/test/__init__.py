
from pytruenas import Namespace
class SmartTest(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'smart.test')

