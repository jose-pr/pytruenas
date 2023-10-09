
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
from enum import Enum

class Alertclasses(ConfigMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'alertclasses')

    AlertclassesEntry = typing.TypedDict('AlertclassesEntry', {
            'id':'int',
            'classes':'dict[str]',
    })
    AlertclassesUpdate = typing.TypedDict('AlertclassesUpdate', {
            'classes':'dict[str]',
    })
    AlertclassesUpdateReturns = typing.TypedDict('AlertclassesUpdateReturns', {
            'id':'int',
            'classes':'dict[str]',
    })
