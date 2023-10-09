
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin
from enum import Enum
import typing
class Smart(
    ConfigMixin,
    Namespace
    ):
    _namespace:typing.Literal['smart']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def config(self, 
    /) -> 'SmartEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        SmartEntry:
            smart_entry
        """
        ...
    @typing.overload
    def update(self, 
        smart_update:'SmartUpdate'={},
    /) -> 'SmartUpdateReturns': 
        """
        Update SMART Service Configuration.
        
        `interval` is an integer value in minutes which defines how often smartd activates to check if any tests
        are configured to run.
        
        `critical`, `informational` and `difference` are integer values on which alerts for SMART are configured if
        the disks temperature crosses the assigned threshold for each respective attribute. They default to 0 which
        indicates they are disabled.

        Parameters
        ----------
        smart_update:
            smart_update
        Returns
        -------
        SmartUpdateReturns:
            smart_update_returns
        """
        ...
    class Powermode(str,Enum):
        NEVER = 'NEVER'
        SLEEP = 'SLEEP'
        STANDBY = 'STANDBY'
        IDLE = 'IDLE'
        ...
    SmartEntry = typing.TypedDict('SmartEntry', {
            'interval':'int',
            'id':'int',
            'powermode':'Powermode',
            'difference':'int',
            'informational':'int',
            'critical':'int',
    })
    SmartUpdate = typing.TypedDict('SmartUpdate', {
            'interval':'int',
            'powermode':'Powermode',
            'difference':'int',
            'informational':'int',
            'critical':'int',
    })
    SmartUpdateReturns = typing.TypedDict('SmartUpdateReturns', {
            'interval':'int',
            'id':'int',
            'powermode':'Powermode',
            'difference':'int',
            'informational':'int',
            'critical':'int',
    })
