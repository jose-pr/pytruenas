
from pytruenas.base import Namespace

import typing
from enum import Enum

class Directoryservices(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'directoryservices')

    class Activedirectory(str,Enum):
        DISABLED = 'DISABLED'
        FAULTED = 'FAULTED'
        LEAVING = 'LEAVING'
        JOINING = 'JOINING'
        HEALTHY = 'HEALTHY'
        ...
    DirectoryServicesStates = typing.TypedDict('DirectoryServicesStates', {
            'activedirectory':'Activedirectory',
            'ldap':'Ldap',
    })
    class Ldap(str,Enum):
        DISABLED = 'DISABLED'
        FAULTED = 'FAULTED'
        LEAVING = 'LEAVING'
        JOINING = 'JOINING'
        HEALTHY = 'HEALTHY'
        ...
