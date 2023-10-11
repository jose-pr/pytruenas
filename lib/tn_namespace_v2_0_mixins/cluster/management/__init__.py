
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
