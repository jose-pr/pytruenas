
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class NetworkConfiguration(Namespace):
    _namespace:_ty.Literal['network.configuration']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def activity_choices(self, 
    /) -> 'list': 
        """
        Returns allowed/forbidden network activity choices.

        Parameters
        ----------
        Returns
        -------
        list:
            activity_choices
        """
        ...
    @_ty.overload
    def config(self, 
    /) -> 'dict[str]': 
        """
        

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            network_configuration_entry
        """
        ...
    @_ty.overload
    def update(self, 
        global_configuration_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update Network Configuration Service configuration.
        
        `ipv4gateway` if set is used instead of the default gateway provided by DHCP.
        
        `nameserver1` is primary DNS server.
        
        `nameserver2` is secondary DNS server.
        
        `nameserver3` is tertiary DNS server.
        
        `httpproxy` attribute must be provided if a proxy is to be used for network operations.
        
        `service_announcement` determines the broadcast protocols that will be used to advertise the server.
        `netbios` enables the NetBIOS name server (NBNS), which starts concurrently with the SMB service. SMB clients
        will only perform NBNS lookups if SMB1 is enabled. NBNS may be required for legacy SMB clients.
        `mdns` enables multicast DNS service announcements for enabled services. `wsd` enables Web Service
        Discovery support.

        Parameters
        ----------
        global_configuration_update:
            global_configuration_update
        Returns
        -------
        dict[str]:
            network_configuration_update_returns
        """
        ...
