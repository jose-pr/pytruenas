
from pytruenas import Namespace
class Certificateauthority(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'certificateauthority')

