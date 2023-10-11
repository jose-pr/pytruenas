
from pytruenas.base import Namespace

import typing
from enum import Enum

class SharingNfs(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'sharing.nfs')

    class Provider(str,Enum):
        SYS = 'SYS'
        KRB5 = 'KRB5'
        KRB5I = 'KRB5I'
        KRB5P = 'KRB5P'
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
    SharingNfsCreateReturns = typing.TypedDict('SharingNfsCreateReturns', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[Provider]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    SharingNfsEntry = typing.TypedDict('SharingNfsEntry', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[Provider]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    SharingNfsUpdateReturns = typing.TypedDict('SharingNfsUpdateReturns', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[Provider]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    SharingnfsCreate = typing.TypedDict('SharingnfsCreate', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[Provider]',
            'enabled':'bool',
    })
    SharingnfsUpdate = typing.TypedDict('SharingnfsUpdate', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[Provider]',
            'enabled':'bool',
    })
