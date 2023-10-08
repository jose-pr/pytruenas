
from pytruenas import Namespace
class Bootenv(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'bootenv')

