
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class CtdbPrivateIps(Namespace):
    _namespace:_ty.Literal['ctdb.private.ips']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        private_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Add a ctdb private address to the cluster
        
        `ip` string representing an IP v4/v6 address
        `node_uuid` uuid of gluster peer assocated with the address
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        private_create:
            private_create
        Returns
        -------
        dict[str]:
            ctdb_private_ips_create_returns
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
        This returns contents of the CTDB nodes file (private IP addresses)
        Explanation of keys are as follows:
        
        `pnn` private node number of the CTDB node. This is a unique identifier
        for this node within the CTDB daemon. It is based on line number in the
        nodes file. Any operation that requires changing node numbers of existing
        nodes will require cluster-wide maintenance window.
        
        `address` the private address of this node. This _must_ be on an isolated
        network as ctdb traffic is unencrypted.
        
        `this_node` boolean indicating whether the entry indicated here is this
        particular cluster node
        
        `node_uuid` the gluster peer uuid of the entry

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
        id:'int',
        private_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update Private IP address from the ctdb cluster with pnn value of `id`.
        
        `id` integer representing the PNN value for the node.
        
        `enable` boolean. When True, enable the node else disable the node.
        
        `node_uuid`. When specified, replace node UUID associated with this nodes entry.
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        id:
            Update Private IP address from the ctdb cluster with pnn value of `id`.
            `id` integer representing the PNN value for the node.
        private_update:
            private_update
        Returns
        -------
        dict[str]:
            ctdb_private_ips_update_returns
        """
        ...
