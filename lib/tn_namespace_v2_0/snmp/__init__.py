
from pytruenas.base import Namespace

import typing
from enum import Enum

class Snmp(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'snmp')

    class V3Authtype(str,Enum):
        _ = ''
        MD5 = 'MD5'
        SHA = 'SHA'
        ...
    class V3Privproto(str,Enum):
        NONE = None
        AES = 'AES'
        DES = 'DES'
        ...
    SnmpEntry = typing.TypedDict('SnmpEntry', {
            'location':'str',
            'contact':'str',
            'traps':'bool',
            'v3':'bool',
            'community':'str',
            'v3_username':'str',
            'v3_authtype':'V3Authtype',
            'v3_password':'str',
            'v3_privproto':'typing.Optional[V3Privproto]',
            'v3_privpassphrase':'typing.Optional[str]',
            'loglevel':'int',
            'options':'str',
            'zilstat':'bool',
            'id':'int',
    })
    SnmpUpdate = typing.TypedDict('SnmpUpdate', {
            'location':'str',
            'contact':'str',
            'traps':'bool',
            'v3':'bool',
            'community':'str',
            'v3_username':'str',
            'v3_authtype':'V3Authtype',
            'v3_password':'str',
            'v3_privproto':'typing.Optional[V3Privproto]',
            'v3_privpassphrase':'typing.Optional[str]',
            'loglevel':'int',
            'options':'str',
            'zilstat':'bool',
    })
    SnmpUpdateReturns = typing.TypedDict('SnmpUpdateReturns', {
            'location':'str',
            'contact':'str',
            'traps':'bool',
            'v3':'bool',
            'community':'str',
            'v3_username':'str',
            'v3_authtype':'V3Authtype',
            'v3_password':'str',
            'v3_privproto':'typing.Optional[V3Privproto]',
            'v3_privpassphrase':'typing.Optional[str]',
            'loglevel':'int',
            'options':'str',
            'zilstat':'bool',
            'id':'int',
    })
