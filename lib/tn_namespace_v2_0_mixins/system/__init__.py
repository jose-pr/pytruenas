
from pytruenas.base import Namespace

import typing
from enum import Enum

class System(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'system')

    class ProductRunningEnvironment(str,Enum):
        DEFAULT = 'DEFAULT'
        EC2 = 'EC2'
        ...
    class Feature(str,Enum):
        DEDUP = 'DEDUP'
        FIBRECHANNEL = 'FIBRECHANNEL'
        VM = 'VM'
        ...
    SystemInfo = typing.TypedDict('SystemInfo', {
            'version':'str',
            'buildtime':'str',
            'hostname':'str',
            'physmem':'int',
            'model':'str',
            'cores':'int',
            'physical_cores':'int',
            'loadavg':'list',
            'uptime':'str',
            'uptime_seconds':'float',
            'system_serial':'typing.Optional[str]',
            'system_product':'typing.Optional[str]',
            'system_product_version':'typing.Optional[str]',
            'license':'dict[str]',
            'boottime':'str',
            'datetime':'str',
            'birthday':'typing.Optional[str]',
            'timezone':'str',
            'system_manufacturer':'typing.Optional[str]',
            'ecc_memory':'bool',
    })
    SystemReboot = typing.TypedDict('SystemReboot', {
            'delay':'int',
    })
    SystemShutdown = typing.TypedDict('SystemShutdown', {
            'delay':'int',
    })
    class SystemState(str,Enum):
        SHUTTINGDOWN = 'SHUTTING_DOWN'
        READY = 'READY'
        BOOTING = 'BOOTING'
        ...
