
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Ups(
    Namespace
    ):
    _namespace:typing.Literal['ups']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def config(self, 
    /) -> 'UpsEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        UpsEntry:
            ups_entry
        """
        ...
    @typing.overload
    def driver_choices(self, 
    /) -> 'dict[str]': 
        """
        Returns choices of UPS drivers supported by the system.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            Example(s):
            ```
            {
                "blazer_ser$CPM-800": "WinPower ups 2 CPM-800 (blazer_ser)"
            }
            ```
        """
        ...
    @typing.overload
    def port_choices(self, 
    /) -> 'list[str]': 
        """
        

        Parameters
        ----------
        Returns
        -------
        list[str]:
            port_choices
        """
        ...
    @typing.overload
    def update(self, 
        ups_update:'UpsUpdate'={},
    /) -> 'UpsUpdateReturns': 
        """
        Update UPS Service Configuration.
        
        `powerdown` when enabled, sets UPS to power off after shutting down the system.
        
        `nocommwarntime` is a value in seconds which makes UPS Service wait the specified seconds before alerting that
        the Service cannot reach configured UPS.
        
        `shutdowntimer` is a value in seconds which tells the Service to wait specified seconds for the UPS before
        initiating a shutdown. This only applies when `shutdown` is set to "BATT".
        
        `shutdowncmd` is the command which is executed to initiate a shutdown. It defaults to "poweroff".

        Parameters
        ----------
        ups_update:
            ups_update
        Returns
        -------
        UpsUpdateReturns:
            ups_update_returns
        """
        ...
    class Mode(str,Enum):
        MASTER = 'MASTER'
        SLAVE = 'SLAVE'
        ...
    class Shutdown(str,Enum):
        LOWBATT = 'LOWBATT'
        BATT = 'BATT'
        ...
    UpsEntry = typing.TypedDict('UpsEntry', {
            'powerdown':'bool',
            'rmonitor':'bool',
            'id':'int',
            'nocommwarntime':'typing.Optional[int]',
            'remoteport':'int',
            'shutdowntimer':'int',
            'hostsync':'int',
            'description':'str',
            'driver':'str',
            'extrausers':'str',
            'identifier':'str',
            'mode':'Mode',
            'monpwd':'str',
            'monuser':'str',
            'options':'str',
            'optionsupsd':'str',
            'port':'str',
            'remotehost':'str',
            'shutdown':'Shutdown',
            'shutdowncmd':'typing.Optional[str]',
            'complete_identifier':'str',
    })
    UpsUpdate = typing.TypedDict('UpsUpdate', {
            'powerdown':'bool',
            'rmonitor':'bool',
            'nocommwarntime':'typing.Optional[int]',
            'remoteport':'int',
            'shutdowntimer':'int',
            'hostsync':'int',
            'description':'str',
            'driver':'str',
            'extrausers':'str',
            'identifier':'str',
            'mode':'Mode',
            'monpwd':'str',
            'monuser':'str',
            'options':'str',
            'optionsupsd':'str',
            'port':'str',
            'remotehost':'str',
            'shutdown':'Shutdown',
            'shutdowncmd':'typing.Optional[str]',
    })
    UpsUpdateReturns = typing.TypedDict('UpsUpdateReturns', {
            'powerdown':'bool',
            'rmonitor':'bool',
            'id':'int',
            'nocommwarntime':'typing.Optional[int]',
            'remoteport':'int',
            'shutdowntimer':'int',
            'hostsync':'int',
            'description':'str',
            'driver':'str',
            'extrausers':'str',
            'identifier':'str',
            'mode':'Mode',
            'monpwd':'str',
            'monuser':'str',
            'options':'str',
            'optionsupsd':'str',
            'port':'str',
            'remotehost':'str',
            'shutdown':'Shutdown',
            'shutdowncmd':'typing.Optional[str]',
            'complete_identifier':'str',
    })
