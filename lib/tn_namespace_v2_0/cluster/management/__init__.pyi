
from pytruenas import Namespace, TrueNASClient
import typing
class ClusterManagement(Namespace):
    _namespace:typing.Literal['cluster.management']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def add_nodes(self, 
        add_cluster_nodes:'AddClusterNodes'={},
    /) -> 'ClusterInformation': 
        """
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.
        
        Add one or more peers to an existing TrueNAS cluster.
        
        `new_cluster_nodes` list of proposed cluster nodes to add to existing cluster
        `remote_credential` - credentials with which to authenticate with specified
        node during the setup process.
        `hostname` - hostname of new node. Must be resolvable by all cluster nodes.
        `private_address` - IP address on private dedicated storage network.
        This address will be used for unencrypted backend traffic and must not
        be publicly exposed in any way.
        `brick_path` - local filesystem path where gluster brick will be
        located. We will try to expand the gluster volume underlying our ctdb
        root directory with bricks on every node added to the cluster.
        `options.skip_brick_add` - Non-default parameter to skip adding bricks.
        `options.rebalance_volume` - Non-default parameter to rebalance volume
        after adding node(s) -- NOTE this may be _very_ long-running

        Parameters
        ----------
        add_cluster_nodes:
            add_cluster_nodes
        Returns
        -------
        ClusterInformation:
            cluster_information
        """
        ...
    @typing.overload
    def cluster_create(self, 
        cluster_configuration:'ClusterConfiguration'={},
    /) -> 'ClusterInformation_': 
        """
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.
        
        Create a cluster based on specified payload. Some prior configuration
        is required.
        
        PRE-REQUISITES:
        - Minimum of 3 TrueNAS servers available (this node and two additional
        peers)
        - All members of cluster must have same version of TrueNAS installed.
        - None of the servers may be members of existing clusters or have prior
        cluster-related configuration files populated
        - Private network must be provided for backend (ctdb and glusterfs) traffic
        - All gluster peer hostnames must be resolvable from all cluster nodes
          and lookups return the private address specified in the above payload.
        
        PAYLOAD INFORMATION:
        
        `volume_configuration` -configuration details of gluster volume that
        will be created during cluster creation.
        `local_node_configuration` - the hostname, private_address, and brick path of
        the current cluster node.
        `peers` - list of additional gluster peers with which to form this cluster.
        Peer information includes the following:
        `hostname` - the hostname by which `private_address` will be resolvable
        via lookups on all cluster nodes.
        `private_address` - IP address on private dedicated storage network.
        This address will be used for unencrypted backend traffic and must not
        be publicly exposed in any way.
        `brick_path` - local filesystem path where gluster brick will be located
        when creating the gluster volume specified in `volume_configuration`.
        `remote_credential` - credentials (either username and password or API key)
        for one-time authentication with gluster peer during cluster creation.
        
        RETURNS:
        dictionary containing:
        `gluster_volume` - gluster volume information for created volume
        `gluster_peers` - gluster peer information for gluster cluster
        `ctdb_configuration` - CTDB configuration directory information and
        contents of nodes file.

        Parameters
        ----------
        cluster_configuration:
            cluster_configuration
        Returns
        -------
        ClusterInformation_:
            cluster_information
        """
        ...
    @typing.overload
    def summary(self, 
        summary_options:'SummaryOptions'={},
    /) -> 'Summary': 
        """
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.
        
        This endpoint aggregates relevant cluster-related state into a single
        large return. Generally, it is a good idea to subscribe to cluster events
        which will send events from cluster leader on takeover (and fresh summary).
        
        `include_volumes` - include clustered volume information (default) - may be
        skipped as performance optimization.
        
        Return contains the following:
        `healthy` - whether cluster state is healthy (ctdb.general.healthy)
        `leader` - object containing information about the current cluster leader
        (meaning of items will be described below under `cluster_node`).
        `cluster_nodes` an array of `cluster_node` objects. Note: these will _always_
        be listed in ascending order based on `pnn` value. Cluster leader will be included.
        `cluster_volumes` - an array of clustered (currently glusterfs) volumes
        
        `cluster_node` object representing a single node in the cluster containing
        the following keys:
        
        `pnn` - internal node number.
        `this_node` - whether the node in question is the current node.
        `enabled` - whether the node is enabled or disabled. Node will be disabled prior
        to replacement in the cluster. The final stages of node removal are disruptive
        operations cluster-wide and so a disabled node may be present in summary until
        administrator has maintenance window to finalize removal.
        `uuid` - UUID uniquely identifying the node (glusterfs peer UUID)
        `status` - object containing both ctdb and gluster peer status for node.
        `status.node.flags` - ctdb status flags for node.
        `status.node.partially_online` - ctdb status indicating that node is still coming online.
        `status.peering.connected` - gluster peer status indicating whether peer is connected
        `status.peering.state` - peering state of node
        `status.peering.status` - verbose peer status

        Parameters
        ----------
        summary_options:
            summary_options
        Returns
        -------
        Summary:
            summary
        """
        ...

class AddClusterNodes(typing.TypedDict):
        new_cluster_nodes:'list[ClusterPeer]'
        options:'Options'
        ...
class ClusterPeer(typing.TypedDict):
        remote_credential:'typing.Union[ForwardRef(PlainCred), ForwardRef(AuthenticationToken), ForwardRef(ApiKey)]'
        hostname:'str'
        private_address:'str'
        brick_path:'str'
        ...
class PlainCred(typing.TypedDict):
        username:'str'
        password:'str'
        ...
class AuthenticationToken(typing.TypedDict):
        auth_token:'str'
        ...
class ApiKey(typing.TypedDict):
        api_key:'str'
        ...
class Options(typing.TypedDict):
        skip_brick_add:'bool'
        rebalance_volume:'bool'
        ...
class ClusterInformation(typing.TypedDict):
        gluster_volume:'list[GlusterVolumeEntry]'
        gluster_peers:'list[GlusterPeerEntry]'
        ctdb_configuration:'CtdbConfiguration'
        ...
class GlusterVolumeEntry(typing.TypedDict):
        name:'str'
        uuid:'str'
        type:'str'
        online:'bool'
        ports:'Ports'
        pid:'str'
        size_total:'int'
        size_free:'int'
        size_used:'int'
        inodes_total:'int'
        inodes_free:'int'
        inodes_used:'int'
        device:'str'
        block_size:'str'
        mnt_options:'str'
        fs_name:'str'
        ...
class Ports(typing.TypedDict):
        tcp:'str'
        rdma:'str'
        ...
class GlusterPeerEntry(typing.TypedDict):
        id:'str'
        uuid:'str'
        hostname:'str'
        connected:'str'
        state:'str'
        status:'str'
        ...
class CtdbConfiguration(typing.TypedDict):
        root_dir_config:'RootDirConfig'
        private_ips:'list[CtdbPrivateIp]'
        ...
class RootDirConfig(typing.TypedDict):
        volume_name:'str'
        volume_mountpoint:'str'
        volume_type:'str'
        path:'str'
        mountpoint:'str'
        uuid:'str'
        ...
class CtdbPrivateIp(typing.TypedDict):
        id:'int'
        pnn:'int'
        address:'str'
        enabled:'bool'
        this_node:'bool'
        node_uuid:'str'
        ...
class ClusterConfiguration(typing.TypedDict):
        volume_configuration:'VolumeConfiguration'
        local_node_configuration:'LocalNodeConfiguration'
        peers:'list[ClusterPeer]'
        ...
class VolumeConfiguration(typing.TypedDict):
        name:'str'
        brick_layout:'typing.Union[ForwardRef(ReplicatedBrickLayout), ForwardRef(DispersedBrickLayout), ForwardRef(DistributedBrickLayout)]'
        ...
class ReplicatedBrickLayout(typing.TypedDict):
        replica_distribute:'int'
        ...
class DispersedBrickLayout(typing.TypedDict):
        disperse_data:'int'
        disperse_redundancy:'int'
        disperse_distribute:'int'
        ...
class DistributedBrickLayout(typing.TypedDict):
        distribute_bricks:'int'
        ...
class LocalNodeConfiguration(typing.TypedDict):
        hostname:'str'
        private_address:'str'
        brick_path:'str'
        ...
class ClusterInformation_(typing.TypedDict):
        gluster_volume:'list[GlusterVolumeEntry]'
        gluster_peers:'list[GlusterPeerEntry]'
        ctdb_configuration:'CtdbConfiguration'
        ...
class SummaryOptions(typing.TypedDict):
        include_volumes:'bool'
        ...
class Summary(typing.TypedDict):
        healthy:'bool'
        version:'Version'
        ctdb_root_dir_config:'RootDirConfig'
        leader:'Leader'
        cluster_nodes:'list[ClusterNode]'
        cluster_volumes:'list'
        ...
class Version(typing.TypedDict):
        major:'int'
        minor:'int'
        ...
class Leader(typing.TypedDict):
        pnn:'int'
        this_node:'bool'
        enabled:'bool'
        uuid:'str'
        status:'Status'
        private_address:'str'
        virtual_addresses:'VirtualAddresses'
        ...
class Status(typing.TypedDict):
        node:'Node'
        peering:'Peering'
        ...
class Node(typing.TypedDict):
        flags:'list'
        partially_online:'bool'
        ...
class Peering(typing.TypedDict):
        connected:'str'
        state:'str'
        status:'str'
        ...
class VirtualAddresses(typing.TypedDict):
        configured:'list'
        active:'list'
        ...
class ClusterNode(typing.TypedDict):
        pnn:'int'
        this_node:'bool'
        enabled:'bool'
        uuid:'str'
        status:'Status'
        private_address:'str'
        virtual_addresses:'VirtualAddresses'
        ...