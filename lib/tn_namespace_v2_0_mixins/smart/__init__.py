
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
class Smart(ConfigMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'smart')

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