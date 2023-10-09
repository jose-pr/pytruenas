
from pytruenas.base import Namespace

import typing
class Ldap(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ldap')

    LdapUpdate = typing.TypedDict('LdapUpdate', {
            'hostname':'list',
            'basedn':'str',
            'binddn':'str',
            'bindpw':'str',
            'anonbind':'bool',
            'ssl':'str',
            'certificate':'typing.Optional[int]',
            'validate_certificates':'bool',
            'disable_freenas_cache':'bool',
            'timeout':'int',
            'dns_timeout':'int',
            'kerberos_realm':'typing.Optional[int]',
            'kerberos_principal':'str',
            'has_samba_schema':'bool',
            'auxiliary_parameters':'str',
            'schema':'str',
            'enable':'bool',
    })
