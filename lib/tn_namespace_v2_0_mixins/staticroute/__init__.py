
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class Staticroute(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'staticroute')

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
    StaticrouteCreate = typing.TypedDict('StaticrouteCreate', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
    })
    StaticrouteCreateReturns = typing.TypedDict('StaticrouteCreateReturns', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
            'id':'int',
    })
    StaticrouteEntry = typing.TypedDict('StaticrouteEntry', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
            'id':'int',
    })
    StaticrouteUpdate = typing.TypedDict('StaticrouteUpdate', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
    })
    StaticrouteUpdateReturns = typing.TypedDict('StaticrouteUpdateReturns', {
            'destination':'str',
            'gateway':'str',
            'description':'str',
            'id':'int',
    })
