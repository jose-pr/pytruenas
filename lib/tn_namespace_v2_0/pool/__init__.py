
from pytruenas.base import Namespace

import typing
from enum import Enum

class Pool(Namespace):
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
    class Deduplication(str,Enum):
        NONE = None
        ON = 'ON'
        VERIFY = 'VERIFY'
        OFF = 'OFF'
        ...
    class Checksum(str,Enum):
        NONE = None
        ON = 'ON'
        OFF = 'OFF'
        FLETCHER2 = 'FLETCHER2'
        FLETCHER4 = 'FLETCHER4'
        SHA256 = 'SHA256'
        SHA512 = 'SHA512'
        SKEIN = 'SKEIN'
        EDONR = 'EDONR'
        ...
    class Algorithm(str,Enum):
        AES128CCM = 'AES-128-CCM'
        AES192CCM = 'AES-192-CCM'
        AES256CCM = 'AES-256-CCM'
        AES128GCM = 'AES-128-GCM'
        AES192GCM = 'AES-192-GCM'
        AES256GCM = 'AES-256-GCM'
        ...
    EncryptionOptions = typing.TypedDict('EncryptionOptions', {
            'generate_key':'bool',
            'pbkdf2iters':'int',
            'algorithm':'Algorithm',
            'passphrase':'typing.Optional[str]',
            'key':'typing.Optional[str]',
    })
    class Type(str,Enum):
        DRAID1 = 'DRAID1'
        DRAID2 = 'DRAID2'
        DRAID3 = 'DRAID3'
        RAIDZ1 = 'RAIDZ1'
        RAIDZ2 = 'RAIDZ2'
        RAIDZ3 = 'RAIDZ3'
        MIRROR = 'MIRROR'
        STRIPE = 'STRIPE'
        ...
    Datavdevs = typing.TypedDict('Datavdevs', {
            'type':'Type',
            'disks':'list[str]',
            'draid_data_disks':'int',
            'draid_spare_disks':'int',
    })
    class Type_(str,Enum):
        MIRROR = 'MIRROR'
        STRIPE = 'STRIPE'
        ...
    Specialvdevs = typing.TypedDict('Specialvdevs', {
            'type':'Type_',
            'disks':'list[str]',
    })
    Dedupvdevs = typing.TypedDict('Dedupvdevs', {
            'type':'Type_',
            'disks':'list[str]',
    })
    class Type__(str,Enum):
        STRIPE = 'STRIPE'
        ...
    Cachevdevs = typing.TypedDict('Cachevdevs', {
            'type':'Type__',
            'disks':'list[str]',
    })
    class Type___(str,Enum):
        STRIPE = 'STRIPE'
        MIRROR = 'MIRROR'
        ...
    Logvdevs = typing.TypedDict('Logvdevs', {
            'type':'Type___',
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
            'deduplication':'typing.Optional[Deduplication]',
            'checksum':'typing.Optional[Checksum]',
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
    class Type____(str,Enum):
        FILESYSTEM = 'FILESYSTEM'
        VOLUME = 'VOLUME'
        ...
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
    class Action(str,Enum):
        START = 'START'
        STOP = 'STOP'
        PAUSE = 'PAUSE'
        ...
    Datavdevs_ = typing.TypedDict('Datavdevs_', {
            'type':'Type',
            'disks':'list[str]',
            'draid_data_disks':'int',
            'draid_spare_disks':'int',
    })
    Specialvdevs_ = typing.TypedDict('Specialvdevs_', {
            'type':'Type_',
            'disks':'list[str]',
    })
    Dedupvdevs_ = typing.TypedDict('Dedupvdevs_', {
            'type':'Type_',
            'disks':'list[str]',
    })
    Cachevdevs_ = typing.TypedDict('Cachevdevs_', {
            'type':'Type__',
            'disks':'list[str]',
    })
    Logvdevs_ = typing.TypedDict('Logvdevs_', {
            'type':'Type___',
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
    class Autotrim(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        ...
    PoolUpdate = typing.TypedDict('PoolUpdate', {
            'topology':'Topology__',
            'allow_duplicate_serials':'bool',
            'autotrim':'Autotrim',
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
