
from pytruenas import TrueNASClient
from pytruenas.base import Namespace

import typing
class IpmiChassis(
    Namespace
    ):
    _namespace:typing.Literal['ipmi.chassis']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def identify(self, 
        verb:'str'="ON",
    /) -> None: 
        """
        Toggle the chassis identify light.
        
        `verb`: str if 'ON' turn identify light on. if 'OFF' turn identify light off.

        Parameters
        ----------
        verb:
            verb
        Returns
        -------
        """
        ...
    @typing.overload
    def info(self, 
    /) -> 'dict[str]': 
        """
        Return looks like:
        {
            "system_power": "on",
            "power_overload": "false",
            "interlock": "inactive",
            "power_fault": "false",
            "power_control_fault": "false",
            "power_restore_policy": "Always off",
            "last_power_event": "unknown",
            "chassis_intrusion": "inactive",
            "front_panel_lockout": "inactive",
            "drive_fault": "false",
            "cooling/fan_fault": "false",
            "chassis_identify_state": "off"
        }

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            chassis_info
        """
        ...

