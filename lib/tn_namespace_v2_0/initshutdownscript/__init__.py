
from pytruenas import Namespace
class Initshutdownscript(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'initshutdownscript')

