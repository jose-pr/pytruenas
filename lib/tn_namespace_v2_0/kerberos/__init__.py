
from pytruenas.base import Namespace

import typing
from enum import Enum

class Kerberos(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'kerberos')

    KerberosSettingsUpdate = typing.TypedDict('KerberosSettingsUpdate', {
            'appdefaults_aux':'str',
            'libdefaults_aux':'str',
    })
