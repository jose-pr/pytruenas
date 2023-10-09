
from pytruenas.base import Namespace

import typing
from enum import Enum

class Alertservice(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'alertservice')

    class Level(str,Enum):
        INFO = 'INFO'
        NOTICE = 'NOTICE'
        WARNING = 'WARNING'
        ERROR = 'ERROR'
        CRITICAL = 'CRITICAL'
        ALERT = 'ALERT'
        EMERGENCY = 'EMERGENCY'
        ...
    AlertServiceCreate = typing.TypedDict('AlertServiceCreate', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'level':'Level',
            'enabled':'bool',
    })
    AlertserviceCreateReturns = typing.TypedDict('AlertserviceCreateReturns', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'level':'Level',
            'enabled':'bool',
            'id':'int',
            'type__title':'str',
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
    AlertServiceType = typing.TypedDict('AlertServiceType', {
            'name':'str',
            'title':'str',
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
    AlertserviceEntry = typing.TypedDict('AlertserviceEntry', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'level':'Level',
            'enabled':'bool',
            'id':'int',
            'type__title':'str',
    })
    AlertServiceUpdate = typing.TypedDict('AlertServiceUpdate', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'level':'Level',
            'enabled':'bool',
    })
    AlertserviceUpdateReturns = typing.TypedDict('AlertserviceUpdateReturns', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'level':'Level',
            'enabled':'bool',
            'id':'int',
            'type__title':'str',
    })
