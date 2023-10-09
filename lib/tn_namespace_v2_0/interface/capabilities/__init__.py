
from pytruenas import Namespace
import typing
class InterfaceCapabilities(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'interface.capabilities')

    Capabilties = typing.TypedDict('Capabilties', {
            'enabled':'list[str]',
            'disabled':'list[str]',
            'supported':'list[str]',
    })
    CapabilitiesSet = typing.TypedDict('CapabilitiesSet', {
            'name':'str',
            'capabilties':'list',
            'action':'str',
    })
