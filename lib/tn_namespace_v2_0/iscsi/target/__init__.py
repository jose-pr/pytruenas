
from pytruenas.base import Namespace

import typing
from enum import Enum

class IscsiTarget(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'iscsi.target')

    class Authmethod(str,Enum):
        NONE = 'NONE'
        CHAP = 'CHAP'
        CHAPMUTUAL = 'CHAP_MUTUAL'
        ...
    Group = typing.TypedDict('Group', {
            'portal':'int',
            'initiator':'typing.Optional[int]',
            'authmethod':'Authmethod',
            'auth':'typing.Optional[int]',
    })
    IscsiTargetCreate = typing.TypedDict('IscsiTargetCreate', {
            'name':'str',
            'alias':'typing.Optional[str]',
            'mode':'Mode',
            'groups':'list[Group]',
            'auth_networks':'list[str]',
    })
    IscsiTargetUpdate = typing.TypedDict('IscsiTargetUpdate', {
            'name':'str',
            'alias':'typing.Optional[str]',
            'mode':'Mode',
            'groups':'list[Group]',
            'auth_networks':'list[str]',
    })
    class Mode(str,Enum):
        ISCSI = 'ISCSI'
        FC = 'FC'
        BOTH = 'BOTH'
        ...
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
