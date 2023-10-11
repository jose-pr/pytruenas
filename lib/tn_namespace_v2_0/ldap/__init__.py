
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
    LdapUpdate = typing.TypedDict('LdapUpdate', {
            'hostname':'list',
            'basedn':'str',
            'binddn':'str',
            'bindpw':'str',
            'anonbind':'bool',
            'ssl':'Ssl',
            'certificate':'typing.Optional[int]',
            'validate_certificates':'bool',
            'disable_freenas_cache':'bool',
            'timeout':'int',
            'dns_timeout':'int',
            'kerberos_realm':'typing.Optional[int]',
            'kerberos_principal':'str',
            'has_samba_schema':'bool',
            'auxiliary_parameters':'str',
            'schema':'Schema',
            'enable':'bool',
    })
    class NssInfoLdap(str,Enum):
        RFC2307 = 'RFC2307'
        RFC2307BIS = 'RFC2307BIS'
        ...
    class Schema(str,Enum):
        RFC2307 = 'RFC2307'
        RFC2307BIS = 'RFC2307BIS'
        ...
    class Ssl(str,Enum):
        OFF = 'OFF'
        ON = 'ON'
        STARTTLS = 'START_TLS'
        ...
