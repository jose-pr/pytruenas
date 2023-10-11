
from pytruenas.base import Namespace

import typing
from enum import Enum

class ClusterManagement(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'cluster.management')

    AddClusterNodes = typing.TypedDict('AddClusterNodes', {
            'new_cluster_nodes':'list[ClusterPeer]',
            'options':'Options',
    })
    ClusterPeer = typing.TypedDict('ClusterPeer', {
            'remote_credential':'typing.Union[PlainCred, AuthenticationToken, ApiKey]',
            'hostname':'str',
            'private_address':'str',
            'brick_path':'str',
    })
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
    Options = typing.TypedDict('Options', {
            'skip_brick_add':'bool',
            'rebalance_volume':'bool',
    })
    ClusterInformation = typing.TypedDict('ClusterInformation', {
            'gluster_volume':'list[GlusterVolumeEntry]',
            'gluster_peers':'list[GlusterPeerEntry]',
            'ctdb_configuration':'CtdbConfiguration',
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
    Ports = typing.TypedDict('Ports', {
            'tcp':'str',
            'rdma':'str',
    })
    GlusterPeerEntry = typing.TypedDict('GlusterPeerEntry', {
            'id':'str',
            'uuid':'str',
            'hostname':'str',
            'connected':'str',
            'state':'str',
            'status':'str',
    })
    CtdbConfiguration = typing.TypedDict('CtdbConfiguration', {
            'root_dir_config':'RootDirConfig',
            'private_ips':'list[CtdbPrivateIp]',
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
    ClusterConfiguration = typing.TypedDict('ClusterConfiguration', {
            'volume_configuration':'VolumeConfiguration',
            'local_node_configuration':'LocalNodeConfiguration',
            'peers':'list[ClusterPeer]',
    })
    VolumeConfiguration = typing.TypedDict('VolumeConfiguration', {
            'name':'str',
            'brick_layout':'typing.Union[ReplicatedBrickLayout, DispersedBrickLayout, DistributedBrickLayout]',
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
    LocalNodeConfiguration = typing.TypedDict('LocalNodeConfiguration', {
            'hostname':'str',
            'private_address':'str',
            'brick_path':'str',
    })
    SummaryOptions = typing.TypedDict('SummaryOptions', {
            'include_volumes':'bool',
    })
    Summary = typing.TypedDict('Summary', {
            'healthy':'bool',
            'version':'Version',
            'ctdb_root_dir_config':'CtdbRootDirConfig',
            'leader':'Leader',
            'cluster_nodes':'list[ClusterNode]',
            'cluster_volumes':'list',
    })
    Version = typing.TypedDict('Version', {
            'major':'int',
            'minor':'int',
    })
    CtdbRootDirConfig = typing.TypedDict('CtdbRootDirConfig', {
            'volume_name':'str',
            'volume_mountpoint':'str',
            'volume_type':'str',
            'path':'str',
            'mountpoint':'str',
            'uuid':'str',
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
    Status = typing.TypedDict('Status', {
            'node':'Node',
            'peering':'Peering',
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
    VirtualAddresses = typing.TypedDict('VirtualAddresses', {
            'configured':'list',
            'active':'list',
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
