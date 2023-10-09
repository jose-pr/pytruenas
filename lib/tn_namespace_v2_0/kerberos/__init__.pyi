
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Kerberos(
    Namespace
    ):
    _namespace:typing.Literal['kerberos']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def config(self, 
    /) -> 'dict[str]': 
        """
        

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            kerberos_entry
        """
        ...
    @typing.overload
    def update(self, 
        kerberos_settings_update:'KerberosSettingsUpdate'={},
    /) -> 'dict[str]': 
        """
        `appdefaults_aux` add parameters to "appdefaults" section of the krb5.conf file.
        
        `libdefaults_aux` add parameters to "libdefaults" section of the krb5.conf file.

        Parameters
        ----------
        kerberos_settings_update:
            kerberos_settings_update
        Returns
        -------
        dict[str]:
            kerberos_update_returns
        """
        ...
    KerberosSettingsUpdate = typing.TypedDict('KerberosSettingsUpdate', {
            'appdefaults_aux':'str',
            'libdefaults_aux':'str',
    })
