
from pytruenas.base import Namespace

import typing
from enum import Enum

class Directoryservices(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'directoryservices')

    class DirectoryserviceState(str,Enum):
        DISABLED = 'DISABLED'
        FAULTED = 'FAULTED'
        LEAVING = 'LEAVING'
        JOINING = 'JOINING'
        HEALTHY = 'HEALTHY'
        ...
    DirectoryServicesStates = typing.TypedDict('DirectoryServicesStates', {
            'activedirectory':'DirectoryserviceState',
            'ldap':'DirectoryserviceState',
    })
