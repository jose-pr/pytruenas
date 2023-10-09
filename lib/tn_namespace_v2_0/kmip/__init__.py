
from pytruenas.base import Namespace

import typing
class Kmip(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'kmip')

    KmipEntry = typing.TypedDict('KmipEntry', {
            'id':'int',
            'enabled':'bool',
            'manage_sed_disks':'bool',
            'manage_zfs_keys':'bool',
            'certificate':'typing.Optional[int]',
            'certificate_authority':'typing.Optional[int]',
            'port':'int',
            'server':'typing.Optional[str]',
            'ssl_version':'str',
    })
    SslVersionChoices = typing.TypedDict('SslVersionChoices', {
            'PROTOCOL_TLSv1':'str',
            'PROTOCOL_TLSv1_1':'str',
            'PROTOCOL_TLSv1_2':'str',
    })
    KmipUpdate = typing.TypedDict('KmipUpdate', {
            'enabled':'bool',
            'manage_sed_disks':'bool',
            'manage_zfs_keys':'bool',
            'certificate':'typing.Optional[int]',
            'certificate_authority':'typing.Optional[int]',
            'port':'int',
            'server':'typing.Optional[str]',
            'ssl_version':'str',
            'force_clear':'bool',
            'change_server':'bool',
            'validate':'bool',
    })
    KmipUpdateReturns = typing.TypedDict('KmipUpdateReturns', {
            'id':'int',
            'enabled':'bool',
            'manage_sed_disks':'bool',
            'manage_zfs_keys':'bool',
            'certificate':'typing.Optional[int]',
            'certificate_authority':'typing.Optional[int]',
            'port':'int',
            'server':'typing.Optional[str]',
            'ssl_version':'str',
    })
