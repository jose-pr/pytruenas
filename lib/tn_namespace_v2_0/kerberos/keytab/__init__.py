
from pytruenas.base import Namespace

import typing
from enum import Enum

class KerberosKeytab(Namespace):
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
    KerberosKeytabEntry = typing.TypedDict('KerberosKeytabEntry', {
            'file':'str',
            'name':'str',
            'id':'int',
    })
    KeytabEntry = typing.TypedDict('KeytabEntry', {
            'slot':'int',
            'kvno':'int',
            'principal':'str',
            'etype':'str',
            'etype_deprecated':'bool',
            'date':'str',
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
