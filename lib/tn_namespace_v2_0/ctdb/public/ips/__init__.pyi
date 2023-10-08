
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class CtdbPublicIps(Namespace):
    _namespace:_ty.Literal['ctdb.public.ips']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        public_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Add a ctdb public address to the cluster
        
        `pnn` node number of record to adjust
        `ip` string representing an IP v4/v6 address
        `netmask` integer representing a cidr notated netmask (i.e. 16/24/48/64 etc)
        `interface` string representing a network interface to apply the `ip`
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        public_create:
            public_create
        Returns
        -------
        dict[str]:
            ctdb_public_ips_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        public_ip:'str',
        pnn:'int'=None,
    /) -> 'bool': 
        """
        Remove the specified `address` from the configuration for the node specified by `pnn`.
        If `pnn` is not specified, then the operation applies to the current node.
        In order to remove an address cluster-wide, this method must be called on
        every node where the public IP address is configured.
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        public_ip:
            public_ip
        pnn:
            Remove the specified `address` from the configuration for the node specified by `pnn`.
            If `pnn` is not specified, then the operation applies to the current node.
            In order to remove an address cluster-wide, this method must be called on
            every node where the public IP address is configured.
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
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
    def interface_choices(self, 
        exclude_ifaces:'list'=[],
    /) -> 'list': 
        """
        Retrieve list of available interface choices that can be used for assigning a ctdbd public ip.

        Parameters
        ----------
        exclude_ifaces:
            exclude_ifaces
        Returns
        -------
        list:
            interface_choices
        """
        ...
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
        """
        Retrieve information about configured public IP addresses for the
        ctdb cluster. This call raise a CallError with errno set to ENXIO
        if this node is not in a state where it can provide accurate
        information about cluster. Examples problematic states are:
        
        - ctdb or glusterd are not running on this node
        
        - ctdb shared volume is not mounted

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
