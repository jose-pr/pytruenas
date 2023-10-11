
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class ClusterManagement(
    Namespace
    ):
    _namespace:typing.Literal['cluster.management']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def add_nodes(self, 
        _add_cluster_nodes:'AddClusterNodes',
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
        _cluster_configuration:'ClusterConfiguration',
    /) -> 'ClusterInformation': 
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
        ClusterInformation:
            cluster_information
        """
        ...
    @typing.overload
    def summary(self, 
        _summary_options:'SummaryOptions',
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
    AddClusterNodes = typing.TypedDict('AddClusterNodes', {
            'new_cluster_nodes':'list[ClusterPeer]',
            'options':'Options',
    })
    ApiKey = typing.TypedDict('ApiKey', {
            'api_key':'str',
    })
    AuthenticationToken = typing.TypedDict('AuthenticationToken', {
            'auth_token':'str',
    })
    ClusterConfiguration = typing.TypedDict('ClusterConfiguration', {
            'volume_configuration':'VolumeConfiguration',
            'local_node_configuration':'LocalNodeConfiguration',
            'peers':'list[ClusterPeer]',
    })
    ClusterInformation = typing.TypedDict('ClusterInformation', {
            'gluster_volume':'list[GlusterVolumeEntry]',
            'gluster_peers':'list[GlusterPeerEntry]',
            'ctdb_configuration':'CtdbConfiguration',
    })
    ClusterNode = typing.TypedDict('ClusterNode', {
            'pnn':'int',
            'this_node':'bool',
            'enabled':'bool',
            'uuid':'str',
            'status':'Status',
            'private_address':'str',
            'virtual_addresses':'VirtualAddresses',
    })
    ClusterPeer = typing.TypedDict('ClusterPeer', {
            'remote_credential':'typing.Union[PlainCred, AuthenticationToken, ApiKey]',
            'hostname':'str',
            'private_address':'str',
            'brick_path':'str',
    })
    CtdbConfiguration = typing.TypedDict('CtdbConfiguration', {
            'root_dir_config':'RootDirConfig',
            'private_ips':'list[CtdbPrivateIp]',
    })
    CtdbPrivateIp = typing.TypedDict('CtdbPrivateIp', {
            'id':'int',
            'pnn':'int',
            'address':'str',
            'enabled':'bool',
            'this_node':'bool',
            'node_uuid':'str',
    })
    CtdbRootDirConfig = typing.TypedDict('CtdbRootDirConfig', {
            'volume_name':'str',
            'volume_mountpoint':'str',
            'volume_type':'str',
            'path':'str',
            'mountpoint':'str',
            'uuid':'str',
    })
    DispersedBrickLayout = typing.TypedDict('DispersedBrickLayout', {
            'disperse_data':'int',
            'disperse_redundancy':'int',
            'disperse_distribute':'int',
    })
    DistributedBrickLayout = typing.TypedDict('DistributedBrickLayout', {
            'distribute_bricks':'int',
    })
    GlusterPeerEntry = typing.TypedDict('GlusterPeerEntry', {
            'id':'str',
            'uuid':'str',
            'hostname':'str',
            'connected':'str',
            'state':'str',
            'status':'str',
    })
    GlusterVolumeEntry = typing.TypedDict('GlusterVolumeEntry', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
    })
    Leader = typing.TypedDict('Leader', {
            'pnn':'int',
            'this_node':'bool',
            'enabled':'bool',
            'uuid':'str',
            'status':'Status',
            'private_address':'str',
            'virtual_addresses':'VirtualAddresses',
    })
    LocalNodeConfiguration = typing.TypedDict('LocalNodeConfiguration', {
            'hostname':'str',
            'private_address':'str',
            'brick_path':'str',
    })
    Node = typing.TypedDict('Node', {
            'flags':'list',
            'partially_online':'bool',
    })
    Options = typing.TypedDict('Options', {
            'skip_brick_add':'bool',
            'rebalance_volume':'bool',
    })
    Peering = typing.TypedDict('Peering', {
            'connected':'str',
            'state':'str',
            'status':'str',
    })
    PlainCred = typing.TypedDict('PlainCred', {
            'username':'str',
            'password':'str',
    })
    Ports = typing.TypedDict('Ports', {
            'tcp':'str',
            'rdma':'str',
    })
    ReplicatedBrickLayout = typing.TypedDict('ReplicatedBrickLayout', {
            'replica_distribute':'int',
    })
    RootDirConfig = typing.TypedDict('RootDirConfig', {
            'volume_name':'str',
            'volume_mountpoint':'str',
            'volume_type':'str',
            'path':'str',
            'mountpoint':'str',
            'uuid':'str',
    })
    Status = typing.TypedDict('Status', {
            'node':'Node',
            'peering':'Peering',
    })
    Summary = typing.TypedDict('Summary', {
            'healthy':'bool',
            'version':'Version',
            'ctdb_root_dir_config':'CtdbRootDirConfig',
            'leader':'Leader',
            'cluster_nodes':'list[ClusterNode]',
            'cluster_volumes':'list',
    })
    SummaryOptions = typing.TypedDict('SummaryOptions', {
            'include_volumes':'bool',
    })
    Version = typing.TypedDict('Version', {
            'major':'int',
            'minor':'int',
    })
    VirtualAddresses = typing.TypedDict('VirtualAddresses', {
            'configured':'list',
            'active':'list',
    })
    VolumeConfiguration = typing.TypedDict('VolumeConfiguration', {
            'name':'str',
            'brick_layout':'typing.Union[ReplicatedBrickLayout, DispersedBrickLayout, DistributedBrickLayout]',
    })
