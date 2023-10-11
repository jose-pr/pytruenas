
from pytruenas.base import Namespace

import typing
from enum import Enum

class Smart(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'smart')

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
