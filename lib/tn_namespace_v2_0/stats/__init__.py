
from pytruenas.base import Namespace

import typing
from enum import Enum

class Stats(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'stats')

    DatasetInfo = typing.TypedDict('DatasetInfo', {
            'source':'str',
            'type':'str',
            'datasets':'dict[str]',
            'step':'int',
            'last_update':'int',
    })
    StatsData = typing.TypedDict('StatsData', {
            'source':'str',
            'type':'str',
            'dataset':'str',
            'cf':'str',
    })
    StatsData_ = typing.TypedDict('StatsData_', {
            'about':'str',
            'meta':'dict[str]',
            'data':'list',
    })
    StatsFilter = typing.TypedDict('StatsFilter', {
            'step':'int',
            'start':'str',
            'end':'str',
    })
