
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class IscsiPortal(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'iscsi.portal')

    class DiscoveryAuthmethod(str,Enum):
        NONE = 'NONE'
        CHAP = 'CHAP'
        CHAPMUTUAL = 'CHAP_MUTUAL'
        ...
    Listen = typing.TypedDict('Listen', {
            'ip':'str',
    })
    IscsiportalCreate = typing.TypedDict('IscsiportalCreate', {
            'comment':'str',
            'discovery_authmethod':'DiscoveryAuthmethod',
            'discovery_authgroup':'typing.Optional[int]',
            'listen':'list[Listen]',
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
    IscsiportalUpdate = typing.TypedDict('IscsiportalUpdate', {
            'comment':'str',
            'discovery_authmethod':'DiscoveryAuthmethod',
            'discovery_authgroup':'typing.Optional[int]',
            'listen':'list[Listen]',
    })
