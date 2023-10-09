
from pytruenas import Namespace
import typing
class ClusterManagement(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'cluster.management')

    PlainCred = typing.TypedDict('PlainCred', {
            'username':'str',
            'password':'str',
    })
    AuthenticationToken = typing.TypedDict('AuthenticationToken', {
            'auth_token':'str',
    })
    ApiKey = typing.TypedDict('ApiKey', {
            'api_key':'str',
    })
    ClusterPeer = typing.TypedDict('ClusterPeer', {
            'remote_credential':'typing.Union[ForwardRef(PlainCred), ForwardRef(AuthenticationToken), ForwardRef(ApiKey)]',
            'hostname':'str',
            'private_address':'str',
            'brick_path':'str',
    })
    Options = typing.TypedDict('Options', {
            'skip_brick_add':'bool',
            'rebalance_volume':'bool',
    })
    AddClusterNodes = typing.TypedDict('AddClusterNodes', {
            'new_cluster_nodes':'list[ClusterPeer]',
            'options':'Options',
    })
    Ports = typing.TypedDict('Ports', {
            'tcp':'str',
            'rdma':'str',
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
    GlusterPeerEntry = typing.TypedDict('GlusterPeerEntry', {
            'id':'str',
            'uuid':'str',
            'hostname':'str',
            'connected':'str',
            'state':'str',
            'status':'str',
    })
    RootDirConfig = typing.TypedDict('RootDirConfig', {
            'volume_name':'str',
            'volume_mountpoint':'str',
            'volume_type':'str',
            'path':'str',
            'mountpoint':'str',
            'uuid':'str',
    })
    CtdbPrivateIp = typing.TypedDict('CtdbPrivateIp', {
            'id':'int',
            'pnn':'int',
            'address':'str',
            'enabled':'bool',
            'this_node':'bool',
            'node_uuid':'str',
    })
    CtdbConfiguration = typing.TypedDict('CtdbConfiguration', {
            'root_dir_config':'RootDirConfig',
            'private_ips':'list[CtdbPrivateIp]',
    })
    ClusterInformation = typing.TypedDict('ClusterInformation', {
            'gluster_volume':'list[GlusterVolumeEntry]',
            'gluster_peers':'list[GlusterPeerEntry]',
            'ctdb_configuration':'CtdbConfiguration',
    })
    ReplicatedBrickLayout = typing.TypedDict('ReplicatedBrickLayout', {
            'replica_distribute':'int',
    })
    DispersedBrickLayout = typing.TypedDict('DispersedBrickLayout', {
            'disperse_data':'int',
            'disperse_redundancy':'int',
            'disperse_distribute':'int',
    })
    DistributedBrickLayout = typing.TypedDict('DistributedBrickLayout', {
            'distribute_bricks':'int',
    })
    VolumeConfiguration = typing.TypedDict('VolumeConfiguration', {
            'name':'str',
            'brick_layout':'typing.Union[ForwardRef(ReplicatedBrickLayout), ForwardRef(DispersedBrickLayout), ForwardRef(DistributedBrickLayout)]',
    })
    LocalNodeConfiguration = typing.TypedDict('LocalNodeConfiguration', {
            'hostname':'str',
            'private_address':'str',
            'brick_path':'str',
    })
    PlainCred_ = typing.TypedDict('PlainCred_', {
            'username':'str',
            'password':'str',
    })
    AuthenticationToken_ = typing.TypedDict('AuthenticationToken_', {
            'auth_token':'str',
    })
    ApiKey_ = typing.TypedDict('ApiKey_', {
            'api_key':'str',
    })
    ClusterPeer_ = typing.TypedDict('ClusterPeer_', {
            'remote_credential':'typing.Union[ForwardRef(PlainCred_), ForwardRef(AuthenticationToken_), ForwardRef(ApiKey_)]',
            'hostname':'str',
            'private_address':'str',
            'brick_path':'str',
    })
    ClusterConfiguration = typing.TypedDict('ClusterConfiguration', {
            'volume_configuration':'VolumeConfiguration',
            'local_node_configuration':'LocalNodeConfiguration',
            'peers':'list[ClusterPeer_]',
    })
    Ports_ = typing.TypedDict('Ports_', {
            'tcp':'str',
            'rdma':'str',
    })
    GlusterVolumeEntry_ = typing.TypedDict('GlusterVolumeEntry_', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports_',
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
    GlusterPeerEntry_ = typing.TypedDict('GlusterPeerEntry_', {
            'id':'str',
            'uuid':'str',
            'hostname':'str',
            'connected':'str',
            'state':'str',
            'status':'str',
    })
    RootDirConfig_ = typing.TypedDict('RootDirConfig_', {
            'volume_name':'str',
            'volume_mountpoint':'str',
            'volume_type':'str',
            'path':'str',
            'mountpoint':'str',
            'uuid':'str',
    })
    CtdbPrivateIp_ = typing.TypedDict('CtdbPrivateIp_', {
            'id':'int',
            'pnn':'int',
            'address':'str',
            'enabled':'bool',
            'this_node':'bool',
            'node_uuid':'str',
    })
    CtdbConfiguration_ = typing.TypedDict('CtdbConfiguration_', {
            'root_dir_config':'RootDirConfig_',
            'private_ips':'list[CtdbPrivateIp_]',
    })
    ClusterInformation_ = typing.TypedDict('ClusterInformation_', {
            'gluster_volume':'list[GlusterVolumeEntry_]',
            'gluster_peers':'list[GlusterPeerEntry_]',
            'ctdb_configuration':'CtdbConfiguration_',
    })
    SummaryOptions = typing.TypedDict('SummaryOptions', {
            'include_volumes':'bool',
    })
    Version = typing.TypedDict('Version', {
            'major':'int',
            'minor':'int',
    })
    RootDirConfig__ = typing.TypedDict('RootDirConfig__', {
            'volume_name':'str',
            'volume_mountpoint':'str',
            'volume_type':'str',
            'path':'str',
            'mountpoint':'str',
            'uuid':'str',
    })
    Node = typing.TypedDict('Node', {
            'flags':'list',
            'partially_online':'bool',
    })
    Peering = typing.TypedDict('Peering', {
            'connected':'str',
            'state':'str',
            'status':'str',
    })
    Status = typing.TypedDict('Status', {
            'node':'Node',
            'peering':'Peering',
    })
    VirtualAddresses = typing.TypedDict('VirtualAddresses', {
            'configured':'list',
            'active':'list',
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
    Node_ = typing.TypedDict('Node_', {
            'flags':'list',
            'partially_online':'bool',
    })
    Peering_ = typing.TypedDict('Peering_', {
            'connected':'str',
            'state':'str',
            'status':'str',
    })
    Status_ = typing.TypedDict('Status_', {
            'node':'Node_',
            'peering':'Peering_',
    })
    VirtualAddresses_ = typing.TypedDict('VirtualAddresses_', {
            'configured':'list',
            'active':'list',
    })
    ClusterNode = typing.TypedDict('ClusterNode', {
            'pnn':'int',
            'this_node':'bool',
            'enabled':'bool',
            'uuid':'str',
            'status':'Status_',
            'private_address':'str',
            'virtual_addresses':'VirtualAddresses_',
    })
    Summary = typing.TypedDict('Summary', {
            'healthy':'bool',
            'version':'Version',
            'ctdb_root_dir_config':'RootDirConfig__',
            'leader':'Leader',
            'cluster_nodes':'list[ClusterNode]',
            'cluster_volumes':'list',
    })
