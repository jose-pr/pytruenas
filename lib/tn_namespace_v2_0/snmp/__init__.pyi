
from pytruenas import TrueNASClient
from pytruenas.base import Namespace

import typing
class Snmp(
    Namespace
    ):
    _namespace:typing.Literal['snmp']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def config(self, 
    /) -> 'SnmpEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        SnmpEntry:
            snmp_entry
        """
        ...
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
    @typing.overload
    def update(self, 
        snmp_update:'SnmpUpdate'={},
    /) -> 'SnmpUpdateReturns': 
        """
        Update SNMP Service Configuration.
        
        `v3` when set enables SNMP version 3.
        
        `v3_username`, `v3_authtype`, `v3_password`, `v3_privproto` and `v3_privpassphrase` are only used when `v3`
        is enabled.

        Parameters
        ----------
        snmp_update:
            snmp_update
        Returns
        -------
        SnmpUpdateReturns:
            snmp_update_returns
        """
        ...
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

