
from pytruenas.base import Namespace

import typing
from enum import Enum

class Initshutdownscript(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'initshutdownscript')

    InitShutdownScriptCreate = typing.TypedDict('InitShutdownScriptCreate', {
            'type':'Type',
            'command':'typing.Optional[str]',
            'script_text':'typing.Optional[str]',
            'script':'typing.Optional[str]',
            'when':'When',
            'enabled':'bool',
            'timeout':'int',
            'comment':'str',
    })
    InitShutdownScriptEntry = typing.TypedDict('InitShutdownScriptEntry', {
            'type':'Type',
            'command':'typing.Optional[str]',
            'script_text':'typing.Optional[str]',
            'script':'typing.Optional[str]',
            'when':'When',
            'enabled':'bool',
            'timeout':'int',
            'comment':'str',
            'id':'int',
    })
    InitshutdownscriptCreateReturns = typing.TypedDict('InitshutdownscriptCreateReturns', {
            'type':'Type',
            'command':'typing.Optional[str]',
            'script_text':'typing.Optional[str]',
            'script':'typing.Optional[str]',
            'when':'When',
            'enabled':'bool',
            'timeout':'int',
            'comment':'str',
            'id':'int',
    })
    InitshutdownscriptUpdate = typing.TypedDict('InitshutdownscriptUpdate', {
            'type':'Type',
            'command':'typing.Optional[str]',
            'script_text':'typing.Optional[str]',
            'script':'typing.Optional[str]',
            'when':'When',
            'enabled':'bool',
            'timeout':'int',
            'comment':'str',
    })
    InitshutdownscriptUpdateReturns = typing.TypedDict('InitshutdownscriptUpdateReturns', {
            'type':'Type',
            'command':'typing.Optional[str]',
            'script_text':'typing.Optional[str]',
            'script':'typing.Optional[str]',
            'when':'When',
            'enabled':'bool',
            'timeout':'int',
            'comment':'str',
            'id':'int',
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
    class Type(str,Enum):
        COMMAND = 'COMMAND'
        SCRIPT = 'SCRIPT'
        ...
    class When(str,Enum):
        PREINIT = 'PREINIT'
        POSTINIT = 'POSTINIT'
        SHUTDOWN = 'SHUTDOWN'
        ...
