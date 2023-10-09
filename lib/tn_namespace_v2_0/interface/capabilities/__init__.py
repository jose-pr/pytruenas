
from pytruenas.base import Namespace

import typing
from enum import Enum

class InterfaceCapabilities(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'interface.capabilities')

    Capabilties = typing.TypedDict('Capabilties', {
            'enabled':'list[str]',
            'disabled':'list[str]',
            'supported':'list[str]',
    })
    class Action(str,Enum):
        ENABLE = 'ENABLE'
        DISABLE = 'DISABLE'
        ...
    CapabilitiesSet = typing.TypedDict('CapabilitiesSet', {
            'name':'str',
            'capabilties':'list',
            'action':'Action',
    })
