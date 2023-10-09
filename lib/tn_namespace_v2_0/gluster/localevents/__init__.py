
from pytruenas import Namespace
import typing
class GlusterLocalevents(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'gluster.localevents')

    AddSecret = typing.TypedDict('AddSecret', {
            'secret':'str',
            'force':'bool',
    })
