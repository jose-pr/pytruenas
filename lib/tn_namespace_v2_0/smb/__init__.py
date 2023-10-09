
from pytruenas.base import Namespace

import typing
class Smb(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'smb')

    Options = typing.TypedDict('Options', {
            'use_kerberos':'bool',
            'output_format':'str',
    })
    GetRemoteAcl = typing.TypedDict('GetRemoteAcl', {
            'server':'str',
            'share':'str',
            'path':'str',
            'username':'str',
            'password':'str',
            'options':'Options',
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
    StatusOptions = typing.TypedDict('StatusOptions', {
            'verbose':'bool',
            'fast':'bool',
            'restrict_user':'str',
            'restrict_session':'str',
    })
    SmbUpdate = typing.TypedDict('SmbUpdate', {
            'netbiosname':'str',
            'netbiosname_b':'str',
            'netbiosalias':'list[str]',
            'workgroup':'str',
            'description':'str',
            'enable_smb1':'bool',
            'unixcharset':'str',
            'loglevel':'str',
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
