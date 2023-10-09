
from pytruenas.base import Namespace

import typing
from enum import Enum

class GlusterLocalevents(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'gluster.localevents')

    AddSecret = typing.TypedDict('AddSecret', {
            'secret':'str',
            'force':'bool',
    })
