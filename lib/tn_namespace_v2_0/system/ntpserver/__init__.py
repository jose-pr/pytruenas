
from pytruenas.base import Namespace

import typing
class SystemNtpserver(Namespace):
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
    SystemNtpserverCreateReturns = typing.TypedDict('SystemNtpserverCreateReturns', {
            'address':'str',
            'burst':'bool',
            'iburst':'bool',
            'prefer':'bool',
            'minpoll':'int',
            'maxpoll':'int',
            'id':'int',
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
    SystemNtpserverUpdateReturns = typing.TypedDict('SystemNtpserverUpdateReturns', {
            'address':'str',
            'burst':'bool',
            'iburst':'bool',
            'prefer':'bool',
            'minpoll':'int',
            'maxpoll':'int',
            'id':'int',
    })
