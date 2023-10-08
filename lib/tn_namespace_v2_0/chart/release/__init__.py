
from pytruenas import Namespace
class ChartRelease(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'chart.release')

