
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class SystemNtpserver(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'system.ntpserver')

    NtpCreate = typing.TypedDict('NtpCreate', {
            'address':'str',
            'burst':'bool',
            'iburst':'bool',
            'prefer':'bool',
            'minpoll':'int',
            'maxpoll':'int',
            'force':'bool',
    })
    NtpEntry = typing.TypedDict('NtpEntry', {
            'address':'str',
            'burst':'bool',
            'iburst':'bool',
            'prefer':'bool',
            'minpoll':'int',
            'maxpoll':'int',
            'id':'int',
    })
    NtpUpdate = typing.TypedDict('NtpUpdate', {
            'address':'str',
            'burst':'bool',
            'iburst':'bool',
            'prefer':'bool',
            'minpoll':'int',
            'maxpoll':'int',
            'force':'bool',
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
    SystemNtpserverCreateReturns = typing.TypedDict('SystemNtpserverCreateReturns', {
            'address':'str',
            'burst':'bool',
            'iburst':'bool',
            'prefer':'bool',
            'minpoll':'int',
            'maxpoll':'int',
            'id':'int',
    })
    SystemNtpserverUpdateReturns = typing.TypedDict('SystemNtpserverUpdateReturns', {
            'address':'str',
            'burst':'bool',
            'iburst':'bool',
            'prefer':'bool',
            'minpoll':'int',
            'maxpoll':'int',
            'id':'int',
    })
