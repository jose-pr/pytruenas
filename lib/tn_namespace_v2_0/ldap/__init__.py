
from pytruenas.base import Namespace

import typing
from enum import Enum

class Ldap(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ldap')

    class DirectoryserviceState(str,Enum):
        DISABLED = 'DISABLED'
        FAULTED = 'FAULTED'
        LEAVING = 'LEAVING'
        JOINING = 'JOINING'
        HEALTHY = 'HEALTHY'
        ...
    class NssInfoLdap(str,Enum):
        RFC2307 = 'RFC2307'
        RFC2307BIS = 'RFC2307BIS'
        ...
    class LdapSslChoice(str,Enum):
        OFF = 'OFF'
        ON = 'ON'
        STARTTLS = 'START_TLS'
        ...
    LdapUpdate = typing.TypedDict('LdapUpdate', {
            'hostname':'list',
            'basedn':'str',
            'binddn':'str',
            'bindpw':'str',
            'anonbind':'bool',
            'ssl':'LdapSslChoice',
            'certificate':'typing.Optional[int]',
            'validate_certificates':'bool',
            'disable_freenas_cache':'bool',
            'timeout':'int',
            'dns_timeout':'int',
            'kerberos_realm':'typing.Optional[int]',
            'kerberos_principal':'str',
            'has_samba_schema':'bool',
            'auxiliary_parameters':'str',
            'schema':'NssInfoLdap',
            'enable':'bool',
    })
