
from pytruenas import Namespace
class ContainerImage(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'container.image')

