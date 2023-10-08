
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Kerberos(Namespace):
    _namespace:_ty.Literal['kerberos']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
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
    @_ty.overload
    def update(self, 
        kerberos_settings_update:'dict[str]'={},
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
