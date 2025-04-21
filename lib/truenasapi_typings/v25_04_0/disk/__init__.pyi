from pytruenas import Namespace as _NS 
class Disk(_NS):
    
    def temperature_alerts(
        names,
    ) -> DiskTemperature_alerts:
        """Returns existing temperature alerts for specified disk `names.`"""
        ...
class DiskTemperature_alerts:
    ... 