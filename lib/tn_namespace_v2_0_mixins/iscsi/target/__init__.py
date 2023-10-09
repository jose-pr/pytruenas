
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
class IscsiTarget(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'iscsi.target')

    Group = typing.TypedDict('Group', {
            'portal':'int',
            'initiator':'typing.Optional[int]',
            'authmethod':'str',
            'auth':'typing.Optional[int]',
    })
    IscsiTargetCreate = typing.TypedDict('IscsiTargetCreate', {
            'name':'str',
            'alias':'typing.Optional[str]',
            'mode':'str',
            'groups':'list[Group]',
            'auth_networks':'list[str]',
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
    Group_ = typing.TypedDict('Group_', {
            'portal':'int',
            'initiator':'typing.Optional[int]',
            'authmethod':'str',
            'auth':'typing.Optional[int]',
    })
    IscsiTargetUpdate = typing.TypedDict('IscsiTargetUpdate', {
            'name':'str',
            'alias':'typing.Optional[str]',
            'mode':'str',
            'groups':'list[Group_]',
            'auth_networks':'list[str]',
    })
