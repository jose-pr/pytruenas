
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class CtdbGeneral(Namespace):
    _namespace:_ty.Literal['ctdb.general']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def healthy(self, 
    /) -> 'bool': 
        """
        Returns a boolean if the ctdb cluster is healthy.

        Parameters
        ----------
        Returns
        -------
        bool:
            status
        """
        ...
    @_ty.overload
    def ips(self, 
        ctdb_ips:'dict[str]'={},
    /) -> 'list': 
        """
        Return a list of public ip addresses in the ctdb cluster.
        
        Public IPs will float between nodes in the cluster and
        should automatically rebalance as nodes become available.

        Parameters
        ----------
        ctdb_ips:
            ctdb_ips
        Returns
        -------
        list:
            ctdb_public_ips
        """
        ...
    @_ty.overload
    def listnodes(self, 
    /) -> 'list': 
        """
        Return a list of nodes in the ctdb cluster.

        Parameters
        ----------
        Returns
        -------
        list:
            nodelist
        """
        ...
    @_ty.overload
    def pnn(self, 
    /) -> 'int': 
        """
        Return node number for this node.
        This value should be static for life of cluster.

        Parameters
        ----------
        Returns
        -------
        int:
            pnn
        """
        ...
    @_ty.overload
    def recovery_master(self, 
    /) -> 'int': 
        """
        Return node number for the recovery master for the cluster.

        Parameters
        ----------
        Returns
        -------
        int:
            recmaster
        """
        ...
    @_ty.overload
    def status(self, 
        ctdb_status:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        List the status of the ctdb cluster.
        
        `all_nodes`: Boolean if True, return status
            for all nodes in the cluster else return
            status of this node.
        
        `nodemap` contains the current nodemap in-memory for ctdb daemon on
        this particular cluster node.
        
        `vnnmap` list of all nodes in the cluster that are participating in
        hosting the cluster databases. BANNED nodes are excluded from vnnmap.
        
        `recovery_master` the node number of the cluster node that currently
        holds the cluster recovery lock in the ctdb shared volume. This node
        is responsible for performing full cluster checks and cluster node
        consistency. It is also responsible for performing databse recovery
        procedures. Database recovery related logs will be primarily located
        on this node and so troubleshooting cluster health and recovery
        operations should start here.
        
        `recovery_mode_str` will be either 'NORMAL' or 'RECOVERY' depending
        on whether database recovery is in progress in the cluster.
        
        `recovery_mode_raw` provides raw the internal raw recovery_state of
        ctdbd. Currently defined values are:
        CTDB_RECOVERY_NORMAL 0
        CTDB_RECOVERY_ACTIVE 1
        
        `all_healthy` provides a summary of whether all nodes in internal
        nodelist are healthy. This is a convenience feature and not an
        explicit ctdb client response.

        Parameters
        ----------
        ctdb_status:
            ctdb_status
        Returns
        -------
        dict[str]:
            ctdb_status
        """
        ...
