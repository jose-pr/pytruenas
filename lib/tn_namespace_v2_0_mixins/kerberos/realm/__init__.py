
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class KerberosRealm(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'kerberos.realm')

    KerberosRealmCreate = typing.TypedDict('KerberosRealmCreate', {
            'realm':'str',
            'kdc':'list',
            'admin_server':'list',
            'kpasswd_server':'list',
    })
    KerberosRealmCreateReturns = typing.TypedDict('KerberosRealmCreateReturns', {
            'realm':'str',
            'kdc':'list',
            'admin_server':'list',
            'kpasswd_server':'list',
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
    KerberosRealmEntry = typing.TypedDict('KerberosRealmEntry', {
            'realm':'str',
            'kdc':'list',
            'admin_server':'list',
            'kpasswd_server':'list',
            'id':'int',
    })
    KerberosRealmUpdate = typing.TypedDict('KerberosRealmUpdate', {
            'realm':'str',
            'kdc':'list',
            'admin_server':'list',
            'kpasswd_server':'list',
    })
    KerberosRealmUpdateReturns = typing.TypedDict('KerberosRealmUpdateReturns', {
            'realm':'str',
            'kdc':'list',
            'admin_server':'list',
            'kpasswd_server':'list',
            'id':'int',
    })
