
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class KerberosKeytab(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'kerberos.keytab')

    KerberosKeytabCreate = typing.TypedDict('KerberosKeytabCreate', {
            'file':'str',
            'name':'str',
    })
    KerberosKeytabCreateReturns = typing.TypedDict('KerberosKeytabCreateReturns', {
            'file':'str',
            'name':'str',
            'id':'int',
    })
    KerberosKeytabEntry = typing.TypedDict('KerberosKeytabEntry', {
            'file':'str',
            'name':'str',
            'id':'int',
    })
    KerberosKeytabUpdate = typing.TypedDict('KerberosKeytabUpdate', {
            'file':'str',
            'name':'str',
    })
    KerberosKeytabUpdateReturns = typing.TypedDict('KerberosKeytabUpdateReturns', {
            'file':'str',
            'name':'str',
            'id':'int',
    })
    KeytabData = typing.TypedDict('KeytabData', {
            'name':'str',
    })
    KeytabEntry = typing.TypedDict('KeytabEntry', {
            'slot':'int',
            'kvno':'int',
            'principal':'str',
            'etype':'str',
            'etype_deprecated':'bool',
            'date':'str',
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
