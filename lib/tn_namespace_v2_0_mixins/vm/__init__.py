
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class Vm(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'vm')

    BootloaderOptions = typing.TypedDict('BootloaderOptions', {
            'UEFI':'UEFI',
            'UEFI_CSM':'UEFICSM',
    })
    class UEFI(str,Enum):
        UEFI = 'UEFI'
        ...
    class UEFICSM(str,Enum):
        LegacyBIOS = 'Legacy BIOS'
        ...
    VmCreate = typing.TypedDict('VmCreate', {
            'command_line_args':'str',
            'cpu_mode':'CpuMode',
            'cpu_model':'typing.Optional[str]',
            'name':'str',
            'description':'str',
            'vcpus':'int',
            'cores':'int',
            'threads':'int',
            'cpuset':'typing.Optional[str]',
            'nodeset':'typing.Optional[str]',
            'pin_vcpus':'bool',
            'suspend_on_snapshot':'bool',
            'trusted_platform_module':'bool',
            'memory':'int',
            'min_memory':'typing.Optional[int]',
            'hyperv_enlightenments':'bool',
            'bootloader':'Bootloader',
            'bootloader_ovmf':'str',
            'autostart':'bool',
            'hide_from_msr':'bool',
            'ensure_display_device':'bool',
            'time':'Time',
            'shutdown_timeout':'int',
            'arch_type':'typing.Optional[str]',
            'machine_type':'typing.Optional[str]',
            'uuid':'typing.Optional[str]',
    })
    class CpuMode(str,Enum):
        CUSTOM = 'CUSTOM'
        HOSTMODEL = 'HOST-MODEL'
        HOSTPASSTHROUGH = 'HOST-PASSTHROUGH'
        ...
    class Bootloader(str,Enum):
        UEFI = 'UEFI'
        UEFICSM = 'UEFI_CSM'
        ...
    class Time(str,Enum):
        LOCAL = 'LOCAL'
        UTC = 'UTC'
        ...
    VmCreateReturns = typing.TypedDict('VmCreateReturns', {
            'command_line_args':'str',
            'cpu_mode':'CpuMode',
            'cpu_model':'typing.Optional[str]',
            'name':'str',
            'description':'str',
            'vcpus':'int',
            'cores':'int',
            'threads':'int',
            'cpuset':'typing.Optional[str]',
            'nodeset':'typing.Optional[str]',
            'pin_vcpus':'bool',
            'suspend_on_snapshot':'bool',
            'trusted_platform_module':'bool',
            'memory':'int',
            'min_memory':'typing.Optional[int]',
            'hyperv_enlightenments':'bool',
            'bootloader':'Bootloader',
            'bootloader_ovmf':'str',
            'autostart':'bool',
            'hide_from_msr':'bool',
            'ensure_display_device':'bool',
            'time':'Time',
            'shutdown_timeout':'int',
            'arch_type':'typing.Optional[str]',
            'machine_type':'typing.Optional[str]',
            'uuid':'typing.Optional[str]',
            'devices':'list',
            'status':'Status',
            'id':'int',
    })
    Status = typing.TypedDict('Status', {
            'state':'str',
            'pid':'typing.Optional[int]',
            'domain_state':'str',
    })
    VmDelete = typing.TypedDict('VmDelete', {
            'zvols':'bool',
            'force':'bool',
    })
    CpuFlags = typing.TypedDict('CpuFlags', {
            'intel_vmx':'bool',
            'unrestricted_guest':'bool',
            'amd_rvi':'bool',
            'amd_asids':'bool',
    })
    VmDeviceEntry = typing.TypedDict('VmDeviceEntry', {
            'dtype':'Dtype',
            'vm':'int',
            'attributes':'dict[str]',
            'order':'typing.Optional[int]',
            'id':'int',
    })
    class Dtype(str,Enum):
        NIC = 'NIC'
        DISK = 'DISK'
        CDROM = 'CDROM'
        PCI = 'PCI'
        DISPLAY = 'DISPLAY'
        RAW = 'RAW'
        USB = 'USB'
        ...
    Options = typing.TypedDict('Options', {
            'protocol':'Protocol',
    })
    class Protocol(str,Enum):
        HTTP = 'HTTP'
        HTTPS = 'HTTPS'
        ...
    DisplayDevicesUri = typing.TypedDict('DisplayDevicesUri', {
            'error':'typing.Optional[str]',
            'uri':'typing.Optional[str]',
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
    GetVmMemoryInfo = typing.TypedDict('GetVmMemoryInfo', {
            'minimum_memory_requested':'int',
            'total_memory_requested':'int',
            'overcommit_required':'bool',
            'memory_req_fulfilled_after_overcommit':'bool',
            'arc_to_shrink':'typing.Optional[int]',
            'current_arc_max':'int',
            'arc_min':'int',
            'arc_max_after_shrink':'int',
            'actual_vm_requested_memory':'int',
    })
    VmemoryInUse = typing.TypedDict('VmemoryInUse', {
            'RNP':'int',
            'PRD':'int',
            'RPRD':'int',
    })
    AvailableDisplayPort = typing.TypedDict('AvailableDisplayPort', {
            'port':'int',
            'web':'int',
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
    VmEntry = typing.TypedDict('VmEntry', {
            'command_line_args':'str',
            'cpu_mode':'CpuMode',
            'cpu_model':'typing.Optional[str]',
            'name':'str',
            'description':'str',
            'vcpus':'int',
            'cores':'int',
            'threads':'int',
            'cpuset':'typing.Optional[str]',
            'nodeset':'typing.Optional[str]',
            'pin_vcpus':'bool',
            'suspend_on_snapshot':'bool',
            'trusted_platform_module':'bool',
            'memory':'int',
            'min_memory':'typing.Optional[int]',
            'hyperv_enlightenments':'bool',
            'bootloader':'Bootloader',
            'bootloader_ovmf':'str',
            'autostart':'bool',
            'hide_from_msr':'bool',
            'ensure_display_device':'bool',
            'time':'Time',
            'shutdown_timeout':'int',
            'arch_type':'typing.Optional[str]',
            'machine_type':'typing.Optional[str]',
            'uuid':'typing.Optional[str]',
            'devices':'list',
            'status':'Status',
            'id':'int',
    })
    ResolutionChoices = typing.TypedDict('ResolutionChoices', {
            '1920x1200':'_1920x1200',
            '1920x1080':'_1920x1080',
            '1600x1200':'_1600x1200',
            '1600x900':'_1600x900',
            '1400x1050':'_1400x1050',
            '1280x1024':'_1280x1024',
            '1280x720':'_1280x720',
            '1024x768':'_1024x768',
            '800x600':'_800x600',
            '640x480':'_640x480',
    })
    class _1920x1200(str,Enum):
        _1920x1200 = '1920x1200'
        ...
    class _1920x1080(str,Enum):
        _1920x1080 = '1920x1080'
        ...
    class _1600x1200(str,Enum):
        _1600x1200 = '1600x1200'
        ...
    class _1600x900(str,Enum):
        _1600x900 = '1600x900'
        ...
    class _1400x1050(str,Enum):
        _1400x1050 = '1400x1050'
        ...
    class _1280x1024(str,Enum):
        _1280x1024 = '1280x1024'
        ...
    class _1280x720(str,Enum):
        _1280x720 = '1280x720'
        ...
    class _1024x768(str,Enum):
        _1024x768 = '1024x768'
        ...
    class _800x600(str,Enum):
        _800x600 = '800x600'
        ...
    class _640x480(str,Enum):
        _640x480 = '640x480'
        ...
    Options_ = typing.TypedDict('Options_', {
            'overcommit':'bool',
    })
    VmStatus = typing.TypedDict('VmStatus', {
            'state':'str',
            'pid':'typing.Optional[int]',
            'domain_state':'str',
    })
    Options__ = typing.TypedDict('Options__', {
            'force':'bool',
            'force_after_timeout':'bool',
    })
    VmUpdate = typing.TypedDict('VmUpdate', {
            'command_line_args':'str',
            'cpu_mode':'CpuMode',
            'cpu_model':'typing.Optional[str]',
            'name':'str',
            'description':'str',
            'vcpus':'int',
            'cores':'int',
            'threads':'int',
            'cpuset':'typing.Optional[str]',
            'nodeset':'typing.Optional[str]',
            'pin_vcpus':'bool',
            'suspend_on_snapshot':'bool',
            'trusted_platform_module':'bool',
            'memory':'int',
            'min_memory':'typing.Optional[int]',
            'hyperv_enlightenments':'bool',
            'bootloader':'Bootloader',
            'bootloader_ovmf':'str',
            'autostart':'bool',
            'hide_from_msr':'bool',
            'ensure_display_device':'bool',
            'time':'Time',
            'shutdown_timeout':'int',
            'arch_type':'typing.Optional[str]',
            'machine_type':'typing.Optional[str]',
            'uuid':'typing.Optional[str]',
            'id':'int',
    })
    VmUpdateReturns = typing.TypedDict('VmUpdateReturns', {
            'command_line_args':'str',
            'cpu_mode':'CpuMode',
            'cpu_model':'typing.Optional[str]',
            'name':'str',
            'description':'str',
            'vcpus':'int',
            'cores':'int',
            'threads':'int',
            'cpuset':'typing.Optional[str]',
            'nodeset':'typing.Optional[str]',
            'pin_vcpus':'bool',
            'suspend_on_snapshot':'bool',
            'trusted_platform_module':'bool',
            'memory':'int',
            'min_memory':'typing.Optional[int]',
            'hyperv_enlightenments':'bool',
            'bootloader':'Bootloader',
            'bootloader_ovmf':'str',
            'autostart':'bool',
            'hide_from_msr':'bool',
            'ensure_display_device':'bool',
            'time':'Time',
            'shutdown_timeout':'int',
            'arch_type':'typing.Optional[str]',
            'machine_type':'typing.Optional[str]',
            'uuid':'typing.Optional[str]',
            'devices':'list',
            'status':'Status',
            'id':'int',
    })
    VirtualizationDetails = typing.TypedDict('VirtualizationDetails', {
            'supported':'bool',
            'error':'typing.Optional[str]',
    })
