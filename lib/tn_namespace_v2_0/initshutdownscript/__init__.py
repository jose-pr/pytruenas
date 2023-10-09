
from pytruenas.base import Namespace

import typing
class Initshutdownscript(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'initshutdownscript')

    InitShutdownScriptCreate = typing.TypedDict('InitShutdownScriptCreate', {
            'type':'str',
            'command':'typing.Optional[str]',
            'script_text':'typing.Optional[str]',
            'script':'typing.Optional[str]',
            'when':'str',
            'enabled':'bool',
            'timeout':'int',
            'comment':'str',
    })
    InitshutdownscriptCreateReturns = typing.TypedDict('InitshutdownscriptCreateReturns', {
            'type':'str',
            'command':'typing.Optional[str]',
            'script_text':'typing.Optional[str]',
            'script':'typing.Optional[str]',
            'when':'str',
            'enabled':'bool',
            'timeout':'int',
            'comment':'str',
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
    InitShutdownScriptEntry = typing.TypedDict('InitShutdownScriptEntry', {
            'type':'str',
            'command':'typing.Optional[str]',
            'script_text':'typing.Optional[str]',
            'script':'typing.Optional[str]',
            'when':'str',
            'enabled':'bool',
            'timeout':'int',
            'comment':'str',
            'id':'int',
    })
    InitShutdownScriptEntry_ = typing.TypedDict('InitShutdownScriptEntry_', {
            'type':'str',
            'command':'typing.Optional[str]',
            'script_text':'typing.Optional[str]',
            'script':'typing.Optional[str]',
            'when':'str',
            'enabled':'bool',
            'timeout':'int',
            'comment':'str',
            'id':'int',
    })
    InitShutdownScriptEntry__ = typing.TypedDict('InitShutdownScriptEntry__', {
            'type':'str',
            'command':'typing.Optional[str]',
            'script_text':'typing.Optional[str]',
            'script':'typing.Optional[str]',
            'when':'str',
            'enabled':'bool',
            'timeout':'int',
            'comment':'str',
            'id':'int',
    })
    InitshutdownscriptUpdate = typing.TypedDict('InitshutdownscriptUpdate', {
            'type':'str',
            'command':'typing.Optional[str]',
            'script_text':'typing.Optional[str]',
            'script':'typing.Optional[str]',
            'when':'str',
            'enabled':'bool',
            'timeout':'int',
            'comment':'str',
    })
    InitshutdownscriptUpdateReturns = typing.TypedDict('InitshutdownscriptUpdateReturns', {
            'type':'str',
            'command':'typing.Optional[str]',
            'script_text':'typing.Optional[str]',
            'script':'typing.Optional[str]',
            'when':'str',
            'enabled':'bool',
            'timeout':'int',
            'comment':'str',
            'id':'int',
    })
