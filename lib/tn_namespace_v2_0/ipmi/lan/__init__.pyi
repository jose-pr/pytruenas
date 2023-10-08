
from pytruenas import Namespace, TrueNASClient
import typing
class IpmiLan(Namespace):
    _namespace:typing.Literal['ipmi.lan']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def channels(self, 
    /) -> 'list[int]': 
        """
        Return a list of available IPMI channels.

        Parameters
        ----------
        Returns
        -------
        list[int]:
            lan_channels
        """
        ...
    @typing.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'QueryOptionsGetInstance'={},
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
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'list[dict[str]]|dict[str]|int|dict[str]': 
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
        list[dict[str]]:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @typing.overload
    def update(self, 
        channel:'int',
        ipmi_update:'IpmiUpdate'={},
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

class QueryOptionsGetInstance(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class QueryOptions(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class IpmiUpdate(typing.TypedDict):
        ipaddress:'str'
        netmask:'str'
        gateway:'str'
        password:'str'
        dhcp:'bool'
        vlan:'typing.Optional[int]'
        ...