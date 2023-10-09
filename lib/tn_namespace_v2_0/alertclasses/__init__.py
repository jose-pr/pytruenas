
from pytruenas.base import Namespace

import typing
class Alertclasses(Namespace):
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
