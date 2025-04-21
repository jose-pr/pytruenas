from pytruenas import Namespace as _NS 
class FailoverReboot(_NS):
    
    def info(
    ) -> FailoverRebootInfo:
        """"""
        ...
    def other_node(
    ) -> FailoverRebootOther_node:
        """Reboot the other node and wait for it to come back online.

NOTE: This makes very few checks on HA systems. You need to know what you're doing before calling this."""
        ...
class FailoverRebootInfo:
    ...
class FailoverRebootOther_node:
    ... 