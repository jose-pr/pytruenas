
from pytruenas.base import Namespace

import typing
from enum import Enum

class Enclosure(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'enclosure')

    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    class Status(str,Enum):
        CLEAR = 'CLEAR'
        FAULT = 'FAULT'
        IDENTIFY = 'IDENTIFY'
        ...
    EnclosureUpdate = typing.TypedDict('EnclosureUpdate', {
            'label':'str',
    })
