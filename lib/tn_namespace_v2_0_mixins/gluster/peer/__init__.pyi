
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin
from enum import Enum
import typing
class GlusterPeer(
    TableExtMixin,
    Namespace
    ):
    _namespace:typing.Literal['gluster.peer']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        _peer_create:'PeerCreate',
    /) -> 'GlusterPeerCreateReturns': 
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
        GlusterPeerCreateReturns:
            gluster_peer_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        _id:'str',
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
    @typing.overload
    def get_instance(self, 
        _id:'typing.Union[str, int, bool, dict[str], list]',
        _query_options_get_instance:'QueryOptionsGetInstance',
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
    def ips_available(self, 
    /) -> 'list[str]': 
        """
        Return list of VIP(v4/v6) addresses available on the system

        Parameters
        ----------
        Returns
        -------
        list[str]:
            ips
        """
        ...
    @typing.overload
    def query(self, 
        _query_filters:'list[list]',
        _query_options:'QueryOptions',
    /) -> 'typing.Union[list[GlusterPeerEntry], GlusterPeerEntry, int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[GlusterPeerEntry], GlusterPeerEntry, int]:
            
        """
        ...
    @typing.overload
    def status(self, 
        _peer_status:'PeerStatus',
    /) -> 'list[GlusterPeerEntry]': 
        """
        List the status of peers in the Trusted Storage Pool.
        
        `localhost` Boolean if True, include localhost else exclude localhost

        Parameters
        ----------
        peer_status:
            peer_status
        Returns
        -------
        list[GlusterPeerEntry]:
            peers
        """
        ...
    GlusterPeerCreateReturns = typing.TypedDict('GlusterPeerCreateReturns', {
            'id':'str',
            'uuid':'str',
            'hostname':'str',
            'connected':'str',
            'state':'str',
            'status':'str',
    })
    GlusterPeerEntry = typing.TypedDict('GlusterPeerEntry', {
            'id':'str',
            'uuid':'str',
            'hostname':'str',
            'connected':'str',
            'state':'str',
            'status':'str',
    })
    PeerCreate = typing.TypedDict('PeerCreate', {
            'hostname':'str',
            'private_address':'str',
    })
    PeerStatus = typing.TypedDict('PeerStatus', {
            'localhost':'bool',
    })
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
