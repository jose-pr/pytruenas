
from pytruenas.base import Namespace

import typing
from enum import Enum

class Alert(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'alert')

    Alert = typing.TypedDict('Alert', {
            'uuid':'str',
            'source':'str',
            'klass':'str',
            'args':'typing.Union[str, int, bool, dict[str], list]',
            'node':'str',
            'key':'str',
            'datetime':'str',
            'last_occurrence':'str',
            'dismissed':'bool',
            'mail':'typing.Union[str, int, bool, dict[str], list]',
            'text':'str',
            'id':'str',
            'level':'str',
            'formatted':'typing.Optional[str]',
            'one_shot':'bool',
    })
    Category = typing.TypedDict('Category', {
            'id':'str',
            'title':'str',
            'classes':'list[CategoryClass]',
    })
    CategoryClass = typing.TypedDict('CategoryClass', {
            'id':'str',
            'title':'str',
            'level':'str',
            'proactive_support':'bool',
    })
    class Policy(str,Enum):
        IMMEDIATELY = 'IMMEDIATELY'
        HOURLY = 'HOURLY'
        DAILY = 'DAILY'
        NEVER = 'NEVER'
        ...
