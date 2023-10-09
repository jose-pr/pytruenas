
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
from enum import Enum

class Smb(ConfigMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'smb')

    class OutputFormat(str,Enum):
        SMB = 'SMB'
        LOCAL = 'LOCAL'
        ...
    Options = typing.TypedDict('Options', {
            'use_kerberos':'bool',
            'output_format':'OutputFormat',
    })
    GetRemoteAcl = typing.TypedDict('GetRemoteAcl', {
            'server':'str',
            'share':'str',
            'path':'str',
            'username':'str',
            'password':'str',
            'options':'Options',
    })
    class InfoLevel(str,Enum):
        AUTHLOG = 'AUTH_LOG'
        ALL = 'ALL'
        SESSIONS = 'SESSIONS'
        SHARES = 'SHARES'
        LOCKS = 'LOCKS'
        BYTERANGE = 'BYTERANGE'
        NOTIFICATIONS = 'NOTIFICATIONS'
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
    StatusOptions = typing.TypedDict('StatusOptions', {
            'verbose':'bool',
            'fast':'bool',
            'restrict_user':'str',
            'restrict_session':'str',
    })
    class Loglevel(str,Enum):
        NONE = 'NONE'
        MINIMUM = 'MINIMUM'
        NORMAL = 'NORMAL'
        FULL = 'FULL'
        DEBUG = 'DEBUG'
        ...
    SmbUpdate = typing.TypedDict('SmbUpdate', {
            'netbiosname':'str',
            'netbiosname_b':'str',
            'netbiosalias':'list[str]',
            'workgroup':'str',
            'description':'str',
            'enable_smb1':'bool',
            'unixcharset':'str',
            'loglevel':'Loglevel',
            'syslog':'bool',
            'aapl_extensions':'bool',
            'localmaster':'bool',
            'guest':'str',
            'admin_group':'typing.Optional[str]',
            'filemask':'str',
            'dirmask':'str',
            'ntlmv1_auth':'bool',
            'multichannel':'bool',
            'bindip':'list[str]',
            'smb_options':'str',
    })
