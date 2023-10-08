
from pytruenas import Namespace
class Route(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'route')

