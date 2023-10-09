
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
class Activedirectory(ConfigMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'activedirectory')

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
