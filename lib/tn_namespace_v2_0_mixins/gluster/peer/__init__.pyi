
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
class GlusterPeer(
    TableExtMixin,
    Namespace
    ):
    _namespace:typing.Literal['gluster.peer']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        peer_create:'PeerCreate'={},
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
    PeerCreate = typing.TypedDict('PeerCreate', {
            'hostname':'str',
            'private_address':'str',
    })
    GlusterPeerCreateReturns = typing.TypedDict('GlusterPeerCreateReturns', {
            'id':'str',
            'uuid':'str',
            'hostname':'str',
            'connected':'str',
            'state':'str',
            'status':'str',
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
    GlusterPeerEntry = typing.TypedDict('GlusterPeerEntry', {
            'id':'str',
            'uuid':'str',
            'hostname':'str',
            'connected':'str',
            'state':'str',
            'status':'str',
    })
    PeerStatus = typing.TypedDict('PeerStatus', {
            'localhost':'bool',
    })
    @typing.overload
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
    PeerCreate = typing.TypedDict('PeerCreate', {
            'hostname':'str',
            'private_address':'str',
    })
    GlusterPeerCreateReturns = typing.TypedDict('GlusterPeerCreateReturns', {
            'id':'str',
            'uuid':'str',
            'hostname':'str',
            'connected':'str',
            'state':'str',
            'status':'str',
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
    GlusterPeerEntry = typing.TypedDict('GlusterPeerEntry', {
            'id':'str',
            'uuid':'str',
            'hostname':'str',
            'connected':'str',
            'state':'str',
            'status':'str',
    })
    PeerStatus = typing.TypedDict('PeerStatus', {
            'localhost':'bool',
    })
    @typing.overload
    def get_instance(self, 
        id:'typing.Union[str, int, bool, dict[str], list]',
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
    PeerCreate = typing.TypedDict('PeerCreate', {
            'hostname':'str',
            'private_address':'str',
    })
    GlusterPeerCreateReturns = typing.TypedDict('GlusterPeerCreateReturns', {
            'id':'str',
            'uuid':'str',
            'hostname':'str',
            'connected':'str',
            'state':'str',
            'status':'str',
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
    GlusterPeerEntry = typing.TypedDict('GlusterPeerEntry', {
            'id':'str',
            'uuid':'str',
            'hostname':'str',
            'connected':'str',
            'state':'str',
            'status':'str',
    })
    PeerStatus = typing.TypedDict('PeerStatus', {
            'localhost':'bool',
    })
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
    PeerCreate = typing.TypedDict('PeerCreate', {
            'hostname':'str',
            'private_address':'str',
    })
    GlusterPeerCreateReturns = typing.TypedDict('GlusterPeerCreateReturns', {
            'id':'str',
            'uuid':'str',
            'hostname':'str',
            'connected':'str',
            'state':'str',
            'status':'str',
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
    GlusterPeerEntry = typing.TypedDict('GlusterPeerEntry', {
            'id':'str',
            'uuid':'str',
            'hostname':'str',
            'connected':'str',
            'state':'str',
            'status':'str',
    })
    PeerStatus = typing.TypedDict('PeerStatus', {
            'localhost':'bool',
    })
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'typing.Union[list[GlusterPeerEntry], ForwardRef(GlusterPeerEntry), int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[GlusterPeerEntry], ForwardRef(GlusterPeerEntry), int]:
            
        """
        ...
    PeerCreate = typing.TypedDict('PeerCreate', {
            'hostname':'str',
            'private_address':'str',
    })
    GlusterPeerCreateReturns = typing.TypedDict('GlusterPeerCreateReturns', {
            'id':'str',
            'uuid':'str',
            'hostname':'str',
            'connected':'str',
            'state':'str',
            'status':'str',
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
    GlusterPeerEntry = typing.TypedDict('GlusterPeerEntry', {
            'id':'str',
            'uuid':'str',
            'hostname':'str',
            'connected':'str',
            'state':'str',
            'status':'str',
    })
    PeerStatus = typing.TypedDict('PeerStatus', {
            'localhost':'bool',
    })
    @typing.overload
    def status(self, 
        peer_status:'PeerStatus'={},
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
    PeerCreate = typing.TypedDict('PeerCreate', {
            'hostname':'str',
            'private_address':'str',
    })
    GlusterPeerCreateReturns = typing.TypedDict('GlusterPeerCreateReturns', {
            'id':'str',
            'uuid':'str',
            'hostname':'str',
            'connected':'str',
            'state':'str',
            'status':'str',
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
    GlusterPeerEntry = typing.TypedDict('GlusterPeerEntry', {
            'id':'str',
            'uuid':'str',
            'hostname':'str',
            'connected':'str',
            'state':'str',
            'status':'str',
    })
    PeerStatus = typing.TypedDict('PeerStatus', {
            'localhost':'bool',
    })

