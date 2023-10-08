
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class SystemAdvanced(Namespace):
    _namespace:_ty.Literal['system.advanced']
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
            system_advanced_entry
        """
        ...
    @_ty.overload
    def sed_global_password(self, 
    /) -> 'str': 
        """
        Returns configured global SED password.

        Parameters
        ----------
        Returns
        -------
        str:
            sed_global_password
        """
        ...
    @_ty.overload
    def serial_port_choices(self, 
    /) -> 'dict[str]': 
        """
        Get available choices for `serialport`.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            serial_port_choices
        """
        ...
    @_ty.overload
    def syslog_certificate_authority_choices(self, 
    /) -> 'dict[str]': 
        """
        Return choices of certificate authorities which can be used for `syslog_tls_certificate_authority`.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            Syslog Certificate Authority Choices
        """
        ...
    @_ty.overload
    def syslog_certificate_choices(self, 
    /) -> 'dict[str]': 
        """
        Return choices of certificates which can be used for `syslog_tls_certificate`.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            Syslog Certificate Choices
        """
        ...
    @_ty.overload
    def update(self, 
        system_advanced_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update System Advanced Service Configuration.
        
        `consolemenu` should be disabled if the menu at console is not desired. It will default to standard login
        in the console if disabled.
        
        `autotune` when enabled executes autotune script which attempts to optimize the system based on the installed
        hardware.
        
        When `syslogserver` is defined, logs of `sysloglevel` or above are sent.
        
        `consolemsg` is a deprecated attribute and will be removed in further releases. Please, use `consolemsg`
        attribute in the `system.general` plugin.
        
        `isolated_gpu_pci_ids` is a list of PCI ids which are isolated from host system.

        Parameters
        ----------
        system_advanced_update:
            system_advanced_update
        Returns
        -------
        dict[str]:
            system_advanced_update_returns
        """
        ...
    @_ty.overload
    def update_gpu_pci_ids(self, 
        isolated_gpu_pci_ids:'list',
    /) -> None: 
        """
        `isolated_gpu_pci_ids` is a list of PCI ids which are isolated from host system.

        Parameters
        ----------
        isolated_gpu_pci_ids:
            isolated_gpu_pci_ids
        Returns
        -------
        """
        ...
