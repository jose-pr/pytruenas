
from pytruenas.base import Namespace

import typing
from enum import Enum

class Activedirectory(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'activedirectory')

    ActivedirectoryUpdate = typing.TypedDict('ActivedirectoryUpdate', {
            'domainname':'str',
            'bindname':'str',
            'bindpw':'str',
            'verbose_logging':'bool',
            'use_default_domain':'bool',
            'allow_trusted_doms':'bool',
            'allow_dns_updates':'bool',
            'disable_freenas_cache':'bool',
            'restrict_pam':'bool',
            'site':'typing.Optional[str]',
            'kerberos_realm':'typing.Optional[int]',
            'kerberos_principal':'typing.Optional[str]',
            'timeout':'int',
            'dns_timeout':'int',
            'nss_info':'typing.Optional[str]',
            'createcomputer':'str',
            'netbiosname':'str',
            'netbiosname_b':'str',
            'netbiosalias':'list',
            'enable':'bool',
    })
    class DirectoryserviceState(str,Enum):
        DISABLED = 'DISABLED'
        FAULTED = 'FAULTED'
        LEAVING = 'LEAVING'
        JOINING = 'JOINING'
        HEALTHY = 'HEALTHY'
        ...
    DomainInfo = typing.TypedDict('DomainInfo', {
            'LDAP server':'str',
            'LDAP server name':'str',
            'Realm':'str',
            'Bind Path':'str',
            'LDAP port':'int',
            'Server time':'int',
            'KDC server':'str',
            'Server time offset':'int',
            'Last machine account password change':'int',
    })
    KerberosUsernamePassword = typing.TypedDict('KerberosUsernamePassword', {
            'username':'str',
            'password':'str',
    })
    class NssInfoAd(str,Enum):
        SFU = 'SFU'
        SFU20 = 'SFU20'
        RFC2307 = 'RFC2307'
        ...
