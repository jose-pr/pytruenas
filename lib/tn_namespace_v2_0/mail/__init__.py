
from pytruenas import Namespace
class Mail(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'mail')

