
from pytruenas import Namespace
class Truecommand(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'truecommand')

