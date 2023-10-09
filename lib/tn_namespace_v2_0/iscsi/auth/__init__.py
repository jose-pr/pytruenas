
from pytruenas import Namespace
import typing
class IscsiAuth(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'iscsi.auth')

    IscsiAuthCreate = typing.TypedDict('IscsiAuthCreate', {
            'tag':'int',
            'user':'str',
            'secret':'str',
            'peeruser':'str',
            'peersecret':'str',
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
    IscsiAuthUpdate = typing.TypedDict('IscsiAuthUpdate', {
            'tag':'int',
            'user':'str',
            'secret':'str',
            'peeruser':'str',
            'peersecret':'str',
    })
