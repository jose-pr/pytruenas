
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class IpmiLan(Namespace):
    _namespace:_ty.Literal['ipmi.lan']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def channels(self, 
    /) -> 'list': 
        """
        Return a list of available IPMI channels.

        Parameters
        ----------
        Returns
        -------
        list:
            lan_channels
        """
        ...
    @_ty.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'dict[str]'={},
    /) -> None: 
        """
        Returns instance matching `id`. If `id` is not found, Validation error is raised.
        
        Please see `query` method documentation for `options`.

        Parameters
        ----------
        id:
            Returns instance matching `id`. If `id` is not found, Validation error is raised.
        query_options_get_instance:
            query-options-get_instance
        Returns
        -------
        """
        ...
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
        """
        Query available IPMI Channels with `query-filters` and `query-options`.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @_ty.overload
    def update(self, 
        channel:'int',
        ipmi_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update IPMI configuration on channel number `id`.
        
        `ipaddress` is an IPv4 address to be assigned to channel number `id`.
        `netmask` is the subnet mask associated with `ipaddress`.
        `gateway` is an IPv4 address used by `ipaddress` to reach outside the local subnet.
        `password` is a password to be assigned to channel number `id`
        `dhcp` is a boolean. If False, `ipaddress`, `netmask` and `gateway` must be set.
        `vlan` is an integer representing the vlan tag number.

        Parameters
        ----------
        channel:
            channel
        ipmi_update:
            ipmi_update
        Returns
        -------
        dict[str]:
            ipmi_lan_update_returns
        """
        ...
