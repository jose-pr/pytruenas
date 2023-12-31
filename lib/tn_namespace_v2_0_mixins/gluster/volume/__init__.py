
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class GlusterVolume(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'gluster.volume')

    Brick = typing.TypedDict('Brick', {
            'peer_name':'str',
            'peer_path':'str',
    })
    GlusterVolumeCreateReturns = typing.TypedDict('GlusterVolumeCreateReturns', {
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
    GlustervolumeCreate = typing.TypedDict('GlustervolumeCreate', {
            'name':'str',
            'bricks':'list[Brick]',
            'replica':'int',
            'arbiter':'int',
            'disperse':'int',
            'disperse_data':'int',
            'redundancy':'int',
            'force':'bool',
    })
    Ports = typing.TypedDict('Ports', {
            'tcp':'str',
            'rdma':'str',
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
    Volume = typing.TypedDict('Volume', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'status':'str',
            'num_bricks':'int',
            'distribute':'int',
            'stripe':'int',
            'replica':'int',
            'disperse':'int',
            'disperse_redundancy':'int',
            'transport':'int',
            'snapshot_count':'int',
            'bricks':'list',
            'options':'list',
    })
    VolumeInfo = typing.TypedDict('VolumeInfo', {
            'name':'str',
    })
    VolumeOptreset = typing.TypedDict('VolumeOptreset', {
            'name':'str',
            'opt':'str',
            'force':'bool',
    })
    VolumeOptset = typing.TypedDict('VolumeOptset', {
            'name':'str',
            'opts':'dict[str]',
    })
    VolumeQuota = typing.TypedDict('VolumeQuota', {
            'name':'str',
            'enable':'bool',
    })
    VolumeRestart = typing.TypedDict('VolumeRestart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStart = typing.TypedDict('VolumeStart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStatus = typing.TypedDict('VolumeStatus', {
            'name':'str',
            'verbose':'bool',
    })
    VolumeStop = typing.TypedDict('VolumeStop', {
            'name':'str',
            'force':'bool',
    })
