
from pytruenas import Namespace
class Certificate(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'certificate')

