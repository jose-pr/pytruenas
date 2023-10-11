
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
from enum import Enum

class Nfs(ConfigMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'nfs')

    KerberosUsernamePassword = typing.TypedDict('KerberosUsernamePassword', {
            'username':'str',
            'password':'str',
    })
    NfsEntry = typing.TypedDict('NfsEntry', {
            'id':'int',
            'servers':'int',
            'udp':'bool',
            'allow_nonroot':'bool',
            'protocols':'list[Protocol]',
            'v4_v3owner':'bool',
            'v4_krb':'bool',
            'v4_domain':'str',
            'bindip':'list[str]',
            'mountd_port':'typing.Optional[int]',
            'rpcstatd_port':'typing.Optional[int]',
            'rpclockd_port':'typing.Optional[int]',
            'mountd_log':'bool',
            'statd_lockd_log':'bool',
            'v4_krb_enabled':'bool',
            'userd_manage_gids':'bool',
    })
    class Protocol(str,Enum):
        NFSV3 = 'NFSV3'
        NFSV4 = 'NFSV4'
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
    NfsUpdate = typing.TypedDict('NfsUpdate', {
            'servers':'int',
            'udp':'bool',
            'allow_nonroot':'bool',
            'protocols':'list[Protocol]',
            'v4_v3owner':'bool',
            'v4_krb':'bool',
            'v4_domain':'str',
            'bindip':'list[str]',
            'mountd_port':'typing.Optional[int]',
            'rpcstatd_port':'typing.Optional[int]',
            'rpclockd_port':'typing.Optional[int]',
            'mountd_log':'bool',
            'statd_lockd_log':'bool',
            'userd_manage_gids':'bool',
    })
    NfsUpdateReturns = typing.TypedDict('NfsUpdateReturns', {
            'id':'int',
            'servers':'int',
            'udp':'bool',
            'allow_nonroot':'bool',
            'protocols':'list[Protocol]',
            'v4_v3owner':'bool',
            'v4_krb':'bool',
            'v4_domain':'str',
            'bindip':'list[str]',
            'mountd_port':'typing.Optional[int]',
            'rpcstatd_port':'typing.Optional[int]',
            'rpclockd_port':'typing.Optional[int]',
            'mountd_log':'bool',
            'statd_lockd_log':'bool',
            'v4_krb_enabled':'bool',
            'userd_manage_gids':'bool',
    })
