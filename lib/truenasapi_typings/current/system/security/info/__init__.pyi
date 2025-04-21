from pytruenas import Namespace as _NS 
class SystemSecurityInfo(_NS):
    
    def fips_available(
    ) -> SystemSecurityInfoFips_available:
        """Returns a boolean identifying whether or not FIPS mode may be toggled on this system"""
        ...
    def fips_enabled(
    ) -> SystemSecurityInfoFips_enabled:
        """Returns a boolean identifying whether or not FIPS mode has been enabled on this system"""
        ...
class SystemSecurityInfoFips_available:
    ...
class SystemSecurityInfoFips_enabled:
    ... 