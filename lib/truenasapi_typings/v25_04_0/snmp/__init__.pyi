from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Snmp(_NS):
    
    def config(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SnmpConfig:
        """"""
        ...
    def update(self,
        snmp_update:snmp_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SnmpUpdate:
        """Update SNMP Service Configuration.

--- Rules --- Enabling v3: requires v3_username, v3_authtype and v3_password Disabling v3: By itself will retain the v3 user settings and config in the 'private' config, but remove the entry in the public config to block v3 access by that user. Disabling v3 and clearing the v3_username: This will do the actions described in 'Disabling v3' and take the extra step to remove the user from the 'private' config.

The 'v3_*' settings are valid and enforced only when 'v3' is enabled"""
        ...
SnmpConfig = _ty.TypedDict('SnmpConfig', {
    'location': str,
    'contact': str|str,
    'traps': bool,
    'v3': bool,
    'community': _ty.NotRequired[str],
    'v3_username': str,
    'v3_authtype': str,
    'v3_password': str,
    'v3_privproto': _jsonschema.JsonValue|None,
    'v3_privpassphrase': _ty.NotRequired[str|None],
    'loglevel': int,
    'options': str,
    'zilstat': bool,
    'id': int, 
})
snmp_update = _ty.TypedDict('snmp_update', {
    'location': _ty.NotRequired[str],
    'contact': _ty.NotRequired[str|str],
    'traps': _ty.NotRequired[bool],
    'v3': _ty.NotRequired[bool],
    'community': _ty.NotRequired[str],
    'v3_username': _ty.NotRequired[str],
    'v3_authtype': _ty.NotRequired[str],
    'v3_password': _ty.NotRequired[str],
    'v3_privproto': _ty.NotRequired[_jsonschema.JsonValue|None],
    'v3_privpassphrase': _ty.NotRequired[str|None],
    'loglevel': _ty.NotRequired[int],
    'options': _ty.NotRequired[str],
    'zilstat': _ty.NotRequired[bool], 
})
SnmpUpdate = _ty.TypedDict('SnmpUpdate', {
    'location': str,
    'contact': str|str,
    'traps': bool,
    'v3': bool,
    'community': _ty.NotRequired[str],
    'v3_username': str,
    'v3_authtype': str,
    'v3_password': str,
    'v3_privproto': _jsonschema.JsonValue|None,
    'v3_privpassphrase': _ty.NotRequired[str|None],
    'loglevel': int,
    'options': str,
    'zilstat': bool,
    'id': int, 
})