
from pytruenas import Namespace
class WebuiImage(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'webui.image')

