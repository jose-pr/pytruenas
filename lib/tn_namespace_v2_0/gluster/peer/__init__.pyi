
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class GlusterPeer(Namespace):
    _namespace:_ty.Literal['gluster.peer']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        peer_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Add peer to the Trusted Storage Pool.
        
        `hostname` String representing an IP(v4/v6) address or DNS name
        
        `private_address` CTDB private address in ctdb nodes file to associate with this peer. This is
            optimization to create ctdb node concurrently with gluster peer.
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        peer_create:
            peer_create
        Returns
        -------
        dict[str]:
            gluster_peer_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'str',
    /) -> None: 
        """
        Remove peer of `id` from the Trusted Storage Pool.
        
        `id` String representing the uuid of the peer
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        id:
            Remove peer of `id` from the Trusted Storage Pool.
            `id` String representing the uuid of the peer
        Returns
        -------
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
    def ips_available(self, 
    /) -> 'list': 
        """
        Return list of VIP(v4/v6) addresses available on the system

        Parameters
        ----------
        Returns
        -------
        list:
            ips
        """
        ...
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
        """
        

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
    def status(self, 
        peer_status:'dict[str]'={},
    /) -> 'list': 
        """
        List the status of peers in the Trusted Storage Pool.
        
        `localhost` Boolean if True, include localhost else exclude localhost

        Parameters
        ----------
        peer_status:
            peer_status
        Returns
        -------
        list:
            peers
        """
        ...
