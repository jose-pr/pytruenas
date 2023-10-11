
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class Vm(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'vm')

    AvailableDisplayPort = typing.TypedDict('AvailableDisplayPort', {
            'port':'int',
            'web':'int',
    })
    class Bootloader(str,Enum):
        UEFI = 'UEFI'
        UEFICSM = 'UEFI_CSM'
        ...
    BootloaderOptions = typing.TypedDict('BootloaderOptions', {
            'UEFI':'typing.Literal["UEFI"]',
            'UEFI_CSM':'typing.Literal["Legacy BIOS"]',
    })
    CpuFlags = typing.TypedDict('CpuFlags', {
            'intel_vmx':'bool',
            'unrestricted_guest':'bool',
            'amd_rvi':'bool',
            'amd_asids':'bool',
    })
    class CpuMode(str,Enum):
        CUSTOM = 'CUSTOM'
        HOSTMODEL = 'HOST-MODEL'
        HOSTPASSTHROUGH = 'HOST-PASSTHROUGH'
        ...
    DisplayDevicesUri = typing.TypedDict('DisplayDevicesUri', {
            'error':'typing.Optional[str]',
            'uri':'typing.Optional[str]',
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
    Options = typing.TypedDict('Options', {
            'protocol':'Protocol',
    })
    Options_ = typing.TypedDict('Options_', {
            'overcommit':'bool',
    })
    Options__ = typing.TypedDict('Options__', {
            'force':'bool',
            'force_after_timeout':'bool',
    })
    class Protocol(str,Enum):
        HTTP = 'HTTP'
        HTTPS = 'HTTPS'
        ...
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
    ResolutionChoices = typing.TypedDict('ResolutionChoices', {
            '1920x1200':'typing.Literal["1920x1200"]',
            '1920x1080':'typing.Literal["1920x1080"]',
            '1600x1200':'typing.Literal["1600x1200"]',
            '1600x900':'typing.Literal["1600x900"]',
            '1400x1050':'typing.Literal["1400x1050"]',
            '1280x1024':'typing.Literal["1280x1024"]',
            '1280x720':'typing.Literal["1280x720"]',
            '1024x768':'typing.Literal["1024x768"]',
            '800x600':'typing.Literal["800x600"]',
            '640x480':'typing.Literal["640x480"]',
    })
    Status = typing.TypedDict('Status', {
            'state':'str',
            'pid':'typing.Optional[int]',
            'domain_state':'str',
    })
    class Time(str,Enum):
        LOCAL = 'LOCAL'
        UTC = 'UTC'
        ...
    VirtualizationDetails = typing.TypedDict('VirtualizationDetails', {
            'supported':'bool',
            'error':'typing.Optional[str]',
    })
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
    VmDelete = typing.TypedDict('VmDelete', {
            'zvols':'bool',
            'force':'bool',
    })
    VmDeviceEntry = typing.TypedDict('VmDeviceEntry', {
            'dtype':'Dtype',
            'vm':'int',
            'attributes':'dict[str]',
            'order':'typing.Optional[int]',
            'id':'int',
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
    VmStatus = typing.TypedDict('VmStatus', {
            'state':'str',
            'pid':'typing.Optional[int]',
            'domain_state':'str',
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
    VmemoryInUse = typing.TypedDict('VmemoryInUse', {
            'RNP':'int',
            'PRD':'int',
            'RPRD':'int',
    })
