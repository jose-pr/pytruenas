from pytruenas import Namespace as _NS 
class Snmp(_NS):
    
    def config(self,
    ) -> SnmpConfig:
        """"""
        ...
    def update(self,
        snmp_update,
    ) -> SnmpUpdate:
        """Update SNMP Service Configuration.

--- Rules --- Enabling v3: requires v3_username, v3_authtype and v3_password Disabling v3: By itself will retain the v3 user settings and config in the 'private' config, but remove the entry in the public config to block v3 access by that user. Disabling v3 and clearing the v3_username: This will do the actions described in 'Disabling v3' and take the extra step to remove the user from the 'private' config.

The 'v3_*' settings are valid and enforced only when 'v3' is enabled"""
        ...
class SnmpConfig:
    ...
class SnmpUpdate:
    ... 