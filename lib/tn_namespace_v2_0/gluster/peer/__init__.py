
from pytruenas.base import Namespace

import typing
class GlusterPeer(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'gluster.peer')

    PeerCreate = typing.TypedDict('PeerCreate', {
            'hostname':'str',
            'private_address':'str',
    })
    GlusterPeerCreateReturns = typing.TypedDict('GlusterPeerCreateReturns', {
            'id':'str',
            'uuid':'str',
            'hostname':'str',
            'connected':'str',
            'state':'str',
            'status':'str',
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
    GlusterPeerEntry = typing.TypedDict('GlusterPeerEntry', {
            'id':'str',
            'uuid':'str',
            'hostname':'str',
            'connected':'str',
            'state':'str',
            'status':'str',
    })
    PeerStatus = typing.TypedDict('PeerStatus', {
            'localhost':'bool',
    })
