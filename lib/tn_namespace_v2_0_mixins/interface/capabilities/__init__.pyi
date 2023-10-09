
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class InterfaceCapabilities(
    Namespace
    ):
    _namespace:typing.Literal['interface.capabilities']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def get(self, 
        name:'str',
    /) -> 'Capabilties': 
        """
        Return enabled, disabled and supported capabilities (also known as features)
        on a given interface.
        
        `name` String representing name of the interface

        Parameters
        ----------
        name:
            name
        Returns
        -------
        Capabilties:
            capabilties
        """
        ...
    @typing.overload
    def set(self, 
        capabilities_set:'CapabilitiesSet'={},
    /) -> 'list[str]': 
        """
        Enable or Disable capabilties (also known as features) on a given interface.
        
        `name` String representing name of the interface
        `capabilities` List representing capabilities to be acted upon
        `action` String when set to 'ENABLE' will enable `capabilities` else if set
                    to `DISABLE` will disable `capabilities`.

        Parameters
        ----------
        capabilities_set:
            capabilities_set
        Returns
        -------
        list[str]:
            capabilities
        """
        ...
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
