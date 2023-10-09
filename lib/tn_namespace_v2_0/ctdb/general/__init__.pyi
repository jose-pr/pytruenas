
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class CtdbGeneral(
    Namespace
    ):
    _namespace:typing.Literal['ctdb.general']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
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
    @typing.overload
    def ips(self, 
        ctdb_ips:'CtdbIps'={},
    /) -> 'list[CtdbPublicIp]': 
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
        list[CtdbPublicIp]:
            ctdb_public_ips
        """
        ...
    @typing.overload
    def listnodes(self, 
    /) -> 'list[CtdbNode]': 
        """
        Return a list of nodes in the ctdb cluster.

        Parameters
        ----------
        Returns
        -------
        list[CtdbNode]:
            nodelist
        """
        ...
    @typing.overload
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
    @typing.overload
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
    @typing.overload
    def status(self, 
        ctdb_status:'CtdbStatus'={},
    /) -> 'CtdbStatus_': 
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
        CtdbStatus_:
            ctdb_status
        """
        ...
    CtdbIps = typing.TypedDict('CtdbIps', {
            'all_nodes':'bool',
    })
    CtdbInterfaceInfo = typing.TypedDict('CtdbInterfaceInfo', {
            'name':'str',
            'active':'bool',
            'available':'bool',
    })
    CtdbPublicIp = typing.TypedDict('CtdbPublicIp', {
            'public_ip':'str',
            'pnn':'int',
            'interfaces':'list[CtdbInterfaceInfo]',
    })
    class AddressType(str,Enum):
        INET = 'INET'
        INET6 = 'INET6'
        ...
    CtdbNode = typing.TypedDict('CtdbNode', {
            'pnn':'int',
            'address':'str',
            'address_type':'AddressType',
            'enabled':'bool',
            'this_node':'bool',
    })
    CtdbStatus = typing.TypedDict('CtdbStatus', {
            'all_nodes':'bool',
    })
    class Type(str,Enum):
        INET = 'INET'
        INET6 = 'INET6'
        ...
    Address = typing.TypedDict('Address', {
            'type':'Type',
            'address':'str',
    })
    class CtdbStatusFlag(str,Enum):
        DISCONNECTED = 'DISCONNECTED'
        UNHEALTHY = 'UNHEALTHY'
        INACTIVE = 'INACTIVE'
        DISABLED = 'DISABLED'
        STOPPED = 'STOPPED'
        DELETED = 'DELETED'
        BANNED = 'BANNED'
        ...
    CtdbNodemapEntry = typing.TypedDict('CtdbNodemapEntry', {
            'pnn':'int',
            'address':'Address',
            'flags':'list[CtdbStatusFlag]',
            'flags_raw':'int',
            'partially_online':'bool',
            'this_node':'bool',
    })
    Nodemap = typing.TypedDict('Nodemap', {
            'node_count':'int',
            'deleted_node_count':'int',
            'nodes':'list[CtdbNodemapEntry]',
    })
    Object = typing.TypedDict('Object', {
            'hash':'int',
            'lmaster':'int',
    })
    Vnnmap = typing.TypedDict('Vnnmap', {
            'size':'int',
            'generation':'int',
            'entries':'list[Object]',
    })
    class RecoveryModeStr(str,Enum):
        NORMAL = 'NORMAL'
        RECOVERY = 'RECOVERY'
        ...
    CtdbStatus_ = typing.TypedDict('CtdbStatus_', {
            'nodemap':'Nodemap',
            'vnnmap':'Vnnmap',
            'recovery_mode_raw':'int',
            'recovery_mode_str':'RecoveryModeStr',
            'recovery_master':'int',
            'all_healthy':'bool',
    })
