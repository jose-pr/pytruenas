
from pytruenas.base import Namespace

import typing
from enum import Enum

class IscsiTargetextent(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'iscsi.targetextent')

    IscsiTargetextentCreate = typing.TypedDict('IscsiTargetextentCreate', {
            'target':'int',
            'lunid':'typing.Optional[int]',
            'extent':'int',
    })
    IscsiTargetextentUpdate = typing.TypedDict('IscsiTargetextentUpdate', {
            'target':'int',
            'lunid':'int',
            'extent':'int',
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
