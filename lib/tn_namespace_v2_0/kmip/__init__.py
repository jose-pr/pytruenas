
from pytruenas.base import Namespace

import typing
from enum import Enum

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
            'ssl_version':'SslVersion',
    })
    KmipUpdate = typing.TypedDict('KmipUpdate', {
            'enabled':'bool',
            'manage_sed_disks':'bool',
            'manage_zfs_keys':'bool',
            'certificate':'typing.Optional[int]',
            'certificate_authority':'typing.Optional[int]',
            'port':'int',
            'server':'typing.Optional[str]',
            'ssl_version':'SslVersion',
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
            'ssl_version':'SslVersion',
    })
    class PROTOCOLTLSv1(str,Enum):
        PROTOCOLTLSv1 = 'PROTOCOL_TLSv1'
        ...
    class PROTOCOLTLSv11(str,Enum):
        PROTOCOLTLSv11 = 'PROTOCOL_TLSv1_1'
        ...
    class PROTOCOLTLSv12(str,Enum):
        PROTOCOLTLSv12 = 'PROTOCOL_TLSv1_2'
        ...
    class SslVersion(str,Enum):
        PROTOCOLTLSv1 = 'PROTOCOL_TLSv1'
        PROTOCOLTLSv11 = 'PROTOCOL_TLSv1_1'
        PROTOCOLTLSv12 = 'PROTOCOL_TLSv1_2'
        ...
    SslVersionChoices = typing.TypedDict('SslVersionChoices', {
            'PROTOCOL_TLSv1':'PROTOCOLTLSv1',
            'PROTOCOL_TLSv1_1':'PROTOCOLTLSv11',
            'PROTOCOL_TLSv1_2':'PROTOCOLTLSv12',
    })
