
from pytruenas import Namespace
class Cronjob(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'cronjob')

