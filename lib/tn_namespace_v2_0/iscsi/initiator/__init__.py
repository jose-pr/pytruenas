
from pytruenas.base import Namespace

import typing
class IscsiInitiator(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'iscsi.initiator')

    IscsiInitiatorCreate = typing.TypedDict('IscsiInitiatorCreate', {
            'initiators':'list',
            'comment':'str',
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
    IscsiInitiatorUpdate = typing.TypedDict('IscsiInitiatorUpdate', {
            'initiators':'list',
            'comment':'str',
    })
