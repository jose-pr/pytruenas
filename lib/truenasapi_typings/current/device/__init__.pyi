from pytruenas import Namespace as _NS 
class Device(_NS):
    
    def get_info(
        data,
    ) -> DeviceGet_info:
        """Get info for `type` device."""
        ...
class DeviceGet_info:
    ... 