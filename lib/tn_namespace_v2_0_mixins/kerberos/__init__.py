
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
class Kerberos(ConfigMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'kerberos')

    KerberosSettingsUpdate = typing.TypedDict('KerberosSettingsUpdate', {
            'appdefaults_aux':'str',
            'libdefaults_aux':'str',
    })
