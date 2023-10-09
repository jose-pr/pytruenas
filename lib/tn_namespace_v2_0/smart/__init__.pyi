
from pytruenas import TrueNASClient
from pytruenas.base import Namespace

import typing
class Smart(
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
    SmartEntry = typing.TypedDict('SmartEntry', {
            'interval':'int',
            'id':'int',
            'powermode':'str',
            'difference':'int',
            'informational':'int',
            'critical':'int',
    })
    SmartUpdate = typing.TypedDict('SmartUpdate', {
            'interval':'int',
            'powermode':'str',
            'difference':'int',
            'informational':'int',
            'critical':'int',
    })
    SmartUpdateReturns = typing.TypedDict('SmartUpdateReturns', {
            'interval':'int',
            'id':'int',
            'powermode':'str',
            'difference':'int',
            'informational':'int',
            'critical':'int',
    })
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
    SmartEntry = typing.TypedDict('SmartEntry', {
            'interval':'int',
            'id':'int',
            'powermode':'str',
            'difference':'int',
            'informational':'int',
            'critical':'int',
    })
    SmartUpdate = typing.TypedDict('SmartUpdate', {
            'interval':'int',
            'powermode':'str',
            'difference':'int',
            'informational':'int',
            'critical':'int',
    })
    SmartUpdateReturns = typing.TypedDict('SmartUpdateReturns', {
            'interval':'int',
            'id':'int',
            'powermode':'str',
            'difference':'int',
            'informational':'int',
            'critical':'int',
    })

