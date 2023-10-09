
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
class Snmp(ConfigMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'snmp')

    SnmpEntry = typing.TypedDict('SnmpEntry', {
            'location':'str',
            'contact':'str',
            'traps':'bool',
            'v3':'bool',
            'community':'str',
            'v3_username':'str',
            'v3_authtype':'str',
            'v3_password':'str',
            'v3_privproto':'typing.Optional[str]',
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
            'v3_authtype':'str',
            'v3_password':'str',
            'v3_privproto':'typing.Optional[str]',
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
            'v3_authtype':'str',
            'v3_password':'str',
            'v3_privproto':'typing.Optional[str]',
            'v3_privpassphrase':'typing.Optional[str]',
            'loglevel':'int',
            'options':'str',
            'zilstat':'bool',
            'id':'int',
    })
