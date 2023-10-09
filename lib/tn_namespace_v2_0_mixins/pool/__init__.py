
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
class Pool(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'pool')

    PoolAttach = typing.TypedDict('PoolAttach', {
            'target_vdev':'str',
            'new_disk':'str',
            'allow_duplicate_serials':'bool',
    })
    Attachment = typing.TypedDict('Attachment', {
            'type':'str',
            'service':'typing.Optional[str]',
            'attachments':'list[str]',
    })
    EncryptionOptions = typing.TypedDict('EncryptionOptions', {
            'generate_key':'bool',
            'pbkdf2iters':'int',
            'algorithm':'str',
            'passphrase':'typing.Optional[str]',
            'key':'typing.Optional[str]',
    })
    Datavdevs = typing.TypedDict('Datavdevs', {
            'type':'str',
            'disks':'list[str]',
            'draid_data_disks':'int',
            'draid_spare_disks':'int',
    })
    Specialvdevs = typing.TypedDict('Specialvdevs', {
            'type':'str',
            'disks':'list[str]',
    })
    Dedupvdevs = typing.TypedDict('Dedupvdevs', {
            'type':'str',
            'disks':'list[str]',
    })
    Cachevdevs = typing.TypedDict('Cachevdevs', {
            'type':'str',
            'disks':'list[str]',
    })
    Logvdevs = typing.TypedDict('Logvdevs', {
            'type':'str',
            'disks':'list[str]',
    })
    Topology = typing.TypedDict('Topology', {
            'data':'list[Datavdevs]',
            'special':'list[Specialvdevs]',
            'dedup':'list[Dedupvdevs]',
            'cache':'list[Cachevdevs]',
            'log':'list[Logvdevs]',
            'spares':'list[str]',
    })
    PoolCreate = typing.TypedDict('PoolCreate', {
            'name':'str',
            'encryption':'bool',
            'deduplication':'typing.Optional[str]',
            'checksum':'typing.Optional[str]',
            'encryption_options':'EncryptionOptions',
            'topology':'Topology',
            'allow_duplicate_serials':'bool',
    })
    Topology_ = typing.TypedDict('Topology_', {
            'data':'list',
            'log':'list',
            'cache':'list',
            'spare':'list',
            'special':'list',
            'dedup':'list',
    })
    PoolCreateReturns = typing.TypedDict('PoolCreateReturns', {
            'id':'int',
            'name':'str',
            'guid':'str',
            'status':'str',
            'path':'str',
            'scan':'dict[str]',
            'is_upgraded':'bool',
            'healthy':'bool',
            'warning':'bool',
            'status_code':'typing.Optional[str]',
            'status_detail':'typing.Optional[str]',
            'size':'typing.Optional[int]',
            'allocated':'typing.Optional[int]',
            'free':'typing.Optional[int]',
            'freeing':'typing.Optional[int]',
            'fragmentation':'typing.Optional[str]',
            'size_str':'typing.Optional[str]',
            'allocated_str':'typing.Optional[str]',
            'free_str':'typing.Optional[str]',
            'freeing_str':'typing.Optional[str]',
            'autotrim':'dict[str]',
            'topology':'Topology_',
    })
    Options = typing.TypedDict('Options', {
            'label':'str',
    })
    Options_ = typing.TypedDict('Options_', {
            'cascade':'bool',
            'restart_services':'bool',
            'destroy':'bool',
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
    PoolEntry = typing.TypedDict('PoolEntry', {
            'id':'int',
            'name':'str',
            'guid':'str',
            'status':'str',
            'path':'str',
            'scan':'dict[str]',
            'is_upgraded':'bool',
            'healthy':'bool',
            'warning':'bool',
            'status_code':'typing.Optional[str]',
            'status_detail':'typing.Optional[str]',
            'size':'typing.Optional[int]',
            'allocated':'typing.Optional[int]',
            'free':'typing.Optional[int]',
            'freeing':'typing.Optional[int]',
            'fragmentation':'typing.Optional[str]',
            'size_str':'typing.Optional[str]',
            'allocated_str':'typing.Optional[str]',
            'free_str':'typing.Optional[str]',
            'freeing_str':'typing.Optional[str]',
            'autotrim':'dict[str]',
            'topology':'Topology_',
    })
    PoolInfo = typing.TypedDict('PoolInfo', {
            'name':'str',
            'guid':'str',
            'status':'str',
            'hostname':'str',
    })
    PoolImport = typing.TypedDict('PoolImport', {
            'guid':'str',
            'name':'str',
            'enable_attachments':'bool',
    })
    Process = typing.TypedDict('Process', {
            'pid':'int',
            'name':'str',
            'service':'str',
            'cmdline':'str',
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
    PoolEntry_ = typing.TypedDict('PoolEntry_', {
            'id':'int',
            'name':'str',
            'guid':'str',
            'status':'str',
            'path':'str',
            'scan':'dict[str]',
            'is_upgraded':'bool',
            'healthy':'bool',
            'warning':'bool',
            'status_code':'typing.Optional[str]',
            'status_detail':'typing.Optional[str]',
            'size':'typing.Optional[int]',
            'allocated':'typing.Optional[int]',
            'free':'typing.Optional[int]',
            'freeing':'typing.Optional[int]',
            'fragmentation':'typing.Optional[str]',
            'size_str':'typing.Optional[str]',
            'allocated_str':'typing.Optional[str]',
            'free_str':'typing.Optional[str]',
            'freeing_str':'typing.Optional[str]',
            'autotrim':'dict[str]',
            'topology':'Topology_',
    })
    PoolEntry__ = typing.TypedDict('PoolEntry__', {
            'id':'int',
            'name':'str',
            'guid':'str',
            'status':'str',
            'path':'str',
            'scan':'dict[str]',
            'is_upgraded':'bool',
            'healthy':'bool',
            'warning':'bool',
            'status_code':'typing.Optional[str]',
            'status_detail':'typing.Optional[str]',
            'size':'typing.Optional[int]',
            'allocated':'typing.Optional[int]',
            'free':'typing.Optional[int]',
            'freeing':'typing.Optional[int]',
            'fragmentation':'typing.Optional[str]',
            'size_str':'typing.Optional[str]',
            'allocated_str':'typing.Optional[str]',
            'free_str':'typing.Optional[str]',
            'freeing_str':'typing.Optional[str]',
            'autotrim':'dict[str]',
            'topology':'Topology_',
    })
    PoolEntry___ = typing.TypedDict('PoolEntry___', {
            'id':'int',
            'name':'str',
            'guid':'str',
            'status':'str',
            'path':'str',
            'scan':'dict[str]',
            'is_upgraded':'bool',
            'healthy':'bool',
            'warning':'bool',
            'status_code':'typing.Optional[str]',
            'status_detail':'typing.Optional[str]',
            'size':'typing.Optional[int]',
            'allocated':'typing.Optional[int]',
            'free':'typing.Optional[int]',
            'freeing':'typing.Optional[int]',
            'fragmentation':'typing.Optional[str]',
            'size_str':'typing.Optional[str]',
            'allocated_str':'typing.Optional[str]',
            'free_str':'typing.Optional[str]',
            'freeing_str':'typing.Optional[str]',
            'autotrim':'dict[str]',
            'topology':'Topology_',
    })
    Options__ = typing.TypedDict('Options__', {
            'label':'str',
            'disk':'str',
            'force':'bool',
            'preserve_settings':'bool',
    })
    Datavdevs_ = typing.TypedDict('Datavdevs_', {
            'type':'str',
            'disks':'list[str]',
            'draid_data_disks':'int',
            'draid_spare_disks':'int',
    })
    Specialvdevs_ = typing.TypedDict('Specialvdevs_', {
            'type':'str',
            'disks':'list[str]',
    })
    Dedupvdevs_ = typing.TypedDict('Dedupvdevs_', {
            'type':'str',
            'disks':'list[str]',
    })
    Cachevdevs_ = typing.TypedDict('Cachevdevs_', {
            'type':'str',
            'disks':'list[str]',
    })
    Logvdevs_ = typing.TypedDict('Logvdevs_', {
            'type':'str',
            'disks':'list[str]',
    })
    Topology__ = typing.TypedDict('Topology__', {
            'data':'list[Datavdevs_]',
            'special':'list[Specialvdevs_]',
            'dedup':'list[Dedupvdevs_]',
            'cache':'list[Cachevdevs_]',
            'log':'list[Logvdevs_]',
            'spares':'list[str]',
    })
    PoolUpdate = typing.TypedDict('PoolUpdate', {
            'topology':'Topology__',
            'allow_duplicate_serials':'bool',
            'autotrim':'str',
    })
    PoolUpdateReturns = typing.TypedDict('PoolUpdateReturns', {
            'id':'int',
            'name':'str',
            'guid':'str',
            'status':'str',
            'path':'str',
            'scan':'dict[str]',
            'is_upgraded':'bool',
            'healthy':'bool',
            'warning':'bool',
            'status_code':'typing.Optional[str]',
            'status_detail':'typing.Optional[str]',
            'size':'typing.Optional[int]',
            'allocated':'typing.Optional[int]',
            'free':'typing.Optional[int]',
            'freeing':'typing.Optional[int]',
            'fragmentation':'typing.Optional[str]',
            'size_str':'typing.Optional[str]',
            'allocated_str':'typing.Optional[str]',
            'free_str':'typing.Optional[str]',
            'freeing_str':'typing.Optional[str]',
            'autotrim':'dict[str]',
            'topology':'Topology_',
    })
