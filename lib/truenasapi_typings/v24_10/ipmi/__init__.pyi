from pytruenas import Namespace as _NS 
class Ipmi(_NS):
    
    def is_loaded(self,
    ) -> IpmiIs_loaded:
        """Returns a boolean value indicating if /dev/ipmi0 is loaded."""
        ...
class IpmiIs_loaded:
    ... 