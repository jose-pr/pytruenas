
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class Bootenv(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'bootenv')

    Attributes = typing.TypedDict('Attributes', {
            'keep':'bool',
    })
    BootenvCreate = typing.TypedDict('BootenvCreate', {
            'name':'str',
            'source':'str',
    })
    BootenvEntry = typing.TypedDict('BootenvEntry', {
            'id':'str',
            'realname':'str',
            'name':'str',
            'active':'str',
            'activated':'bool',
            'can_activate':'bool',
            'mountpoint':'str',
            'space':'str',
            'created':'str',
            'keep':'bool',
            'rawspace':'int',
    })
    BootenvUpdate = typing.TypedDict('BootenvUpdate', {
            'name':'str',
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
