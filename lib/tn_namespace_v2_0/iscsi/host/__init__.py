
from pytruenas.base import Namespace

import typing
from enum import Enum

class IscsiHost(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'iscsi.host')

    IscsiHostCreate = typing.TypedDict('IscsiHostCreate', {
            'ip':'str',
            'description':'str',
            'iqns':'list[str]',
            'added_automatically':'bool',
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
    IscsiHostUpdate = typing.TypedDict('IscsiHostUpdate', {
            'ip':'str',
            'description':'str',
            'iqns':'list[str]',
            'added_automatically':'bool',
    })
