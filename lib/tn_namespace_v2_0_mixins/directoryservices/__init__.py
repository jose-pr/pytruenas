
from pytruenas.base import Namespace

import typing
class Directoryservices(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'directoryservices')

    DirectoryServicesStates = typing.TypedDict('DirectoryServicesStates', {
            'activedirectory':'str',
            'ldap':'str',
    })
