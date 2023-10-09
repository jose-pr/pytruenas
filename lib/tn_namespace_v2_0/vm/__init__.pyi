
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Vm(
    Namespace
    ):
    _namespace:typing.Literal['vm']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def bootloader_options(self, 
    /) -> 'BootloaderOptions': 
        """
        Supported motherboard firmware options.

        Parameters
        ----------
        Returns
        -------
        BootloaderOptions:
            bootloader_options
        """
        ...
    @typing.overload
    def bootloader_ovmf_choices(self, 
    /) -> 'dict[str]': 
        """
        Retrieve bootloader ovmf choices

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            bootloader_ovmf_choices
        """
        ...
    @typing.overload
    def clone(self, 
        id:'int',
        name:'str'=None,
    /) -> 'bool': 
        """
        Clone the VM `id`.
        
        `name` is an optional parameter for the cloned VM.
        If not provided it will append the next number available to the VM name.

        Parameters
        ----------
        id:
            Clone the VM `id`.
        name:
            name
        Returns
        -------
        bool:
            clone
        """
        ...
    @typing.overload
    def cpu_model_choices(self, 
    /) -> 'dict[str]': 
        """
        Retrieve CPU Model choices which can be used with a VM guest to emulate the CPU in the guest.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            Example(s):
            ```
            {
                "486": "486",
                "pentium": "pentium"
            }
            ```
        """
        ...
    @typing.overload
    def create(self, 
        vm_create:'VmCreate'={},
    /) -> 'VmCreateReturns': 
        """
        Create a Virtual Machine (VM).
        
        Maximum of 16 guest virtual CPUs are allowed. By default, every virtual CPU is configured as a
        separate package. Multiple cores can be configured per CPU by specifying `cores` attributes.
        `vcpus` specifies total number of CPU sockets. `cores` specifies number of cores per socket. `threads`
        specifies number of threads per core.
        
        `ensure_display_device` when set ( the default ) will ensure that the guest always has access to a video device.
        For headless installations like ubuntu server this is required for the guest to operate properly. However
        for cases where consumer would like to use GPU passthrough and does not want a display device added should set
        this to `false`.
        
        `arch_type` refers to architecture type and can be specified for the guest. By default the value is `null` and
        system in this case will choose a reasonable default based on host.
        
        `machine_type` refers to machine type of the guest based on the architecture type selected with `arch_type`.
        By default the value is `null` and system in this case will choose a reasonable default based on `arch_type`
        configuration.
        
        `shutdown_timeout` indicates the time in seconds the system waits for the VM to cleanly shutdown. During system
        shutdown, if the VM hasn't exited after a hardware shutdown signal has been sent by the system within
        `shutdown_timeout` seconds, system initiates poweroff for the VM to stop it.
        
        `hide_from_msr` is a boolean which when set will hide the KVM hypervisor from standard MSR based discovery and
        is useful to enable when doing GPU passthrough.
        
        `hyperv_enlightenments` can be used to enable subset of predefined Hyper-V enlightenments for Windows guests.
        These enlightenments improve performance and enable otherwise missing features.
        
        `suspend_on_snapshot` is a boolean attribute which when enabled will automatically pause/suspend VMs when
        a snapshot is being taken for periodic snapshot tasks. For manual snapshots, if user has specified vms to
        be paused, they will be in that case.

        Parameters
        ----------
        vm_create:
            vm_create
        Returns
        -------
        VmCreateReturns:
            vm_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
        vm_delete:'VmDelete'={},
    /) -> 'bool': 
        """
        Delete a VM.

        Parameters
        ----------
        id:
            id
        vm_delete:
            vm_delete
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
        """
        ...
    @typing.overload
    def flags(self, 
    /) -> 'CpuFlags': 
        """
        Returns a dictionary with CPU flags for the hypervisor.

        Parameters
        ----------
        Returns
        -------
        CpuFlags:
            cpu_flags
        """
        ...
    @typing.overload
    def get_available_memory(self, 
        overcommit:'bool'=False,
    /) -> 'int': 
        """
        Get the current maximum amount of available memory to be allocated for VMs.
        
        In case of `overcommit` being `true`, calculations are done in the following manner:
        1. If a VM has requested 10G but is only consuming 5G, only 5G will be counted
        2. System will consider shrinkable ZFS ARC as free memory ( shrinkable ZFS ARC is current ZFS ARC
           minus ZFS ARC minimum )
        
        In case of `overcommit` being `false`, calculations are done in the following manner:
        1. Complete VM requested memory will be taken into account regardless of how much actual physical
           memory the VM is consuming
        2. System will not consider shrinkable ZFS ARC as free memory
        
        Memory is of course a very "volatile" resource, values may change abruptly between a
        second but I deem it good enough to give the user a clue about how much memory is
        available at the current moment and if a VM should be allowed to be launched.

        Parameters
        ----------
        overcommit:
            In case of `overcommit` being `true`, calculations are done in the following manner:
            1. If a VM has requested 10G but is only consuming 5G, only 5G will be counted
            2. System will consider shrinkable ZFS ARC as free memory ( shrinkable ZFS ARC is current ZFS ARC
               minus ZFS ARC minimum )
            In case of `overcommit` being `false`, calculations are done in the following manner:
            1. Complete VM requested memory will be taken into account regardless of how much actual physical
               memory the VM is consuming
            2. System will not consider shrinkable ZFS ARC as free memory
        Returns
        -------
        int:
            available_memory
        """
        ...
    @typing.overload
    def get_console(self, 
        id:'int',
    /) -> 'str': 
        """
        Get the console device from a given guest.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        str:
            console_device
        """
        ...
    @typing.overload
    def get_display_devices(self, 
        id:'int',
    /) -> 'list[VmDeviceEntry]': 
        """
        Get the display devices from a given guest. If a display device has password configured,
        `attributes.password_configured` will be set to `true`.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        list[VmDeviceEntry]:
            get_display_devices
        """
        ...
    @typing.overload
    def get_display_web_uri(self, 
        id:'int',
        host:'str'="",
        options:'Options'={},
    /) -> 'DisplayDevicesUri': 
        """
        Retrieve Display URI for a given VM or appropriate error if there is no display device available
        or if it is not configured to use web interface

        Parameters
        ----------
        id:
            id
        host:
            host
        options:
            options
        Returns
        -------
        DisplayDevicesUri:
            display_devices_uri
        """
        ...
    @typing.overload
    def get_instance(self, 
        id:'typing.Union[str, int, bool, dict[str], list]',
        query_options_get_instance:'QueryOptionsGetInstance'={},
    /) -> None: 
        """
        Returns instance matching `id`. If `id` is not found, Validation error is raised.
        
        Please see `query` method documentation for `options`.

        Parameters
        ----------
        id:
            Returns instance matching `id`. If `id` is not found, Validation error is raised.
        query_options_get_instance:
            query-options-get_instance
        Returns
        -------
        """
        ...
    @typing.overload
    def get_memory_usage(self, 
        vm_id:'int',
    /) -> 'int': 
        """
        

        Parameters
        ----------
        vm_id:
            vm_id
        Returns
        -------
        int:
            Memory usage of a VM in bytes
        """
        ...
    @typing.overload
    def get_vm_memory_info(self, 
        vm_id:'int',
    /) -> 'GetVmMemoryInfo': 
        """
        Returns memory information for `vm_id` VM if it is going to be started.
        
        All memory attributes are expressed in bytes.

        Parameters
        ----------
        vm_id:
            Returns memory information for `vm_id` VM if it is going to be started.
        Returns
        -------
        GetVmMemoryInfo:
            get_vm_memory_info
        """
        ...
    @typing.overload
    def get_vmemory_in_use(self, 
    /) -> 'VmemoryInUse': 
        """
        The total amount of virtual memory in MB used by guests
        
            Returns a dict with the following information:
                RNP - Running but not provisioned
                PRD - Provisioned but not running
                RPRD - Running and provisioned

        Parameters
        ----------
        Returns
        -------
        VmemoryInUse:
            vmemory_in_use
        """
        ...
    @typing.overload
    def guest_architecture_and_machine_choices(self, 
    /) -> 'dict[str]': 
        """
        Retrieve choices for supported guest architecture types and machine choices.
        
        Keys in the response would be supported guest architecture(s) on the host and their respective values would
        be supported machine type(s) for the specific architecture on the host.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            Example(s):
            ```
            {
                "x86_64": [
                    "pc-i440fx-5.2",
                    "pc-q35-5.2",
                    "pc-i440fx-2.7"
                ],
                "i686": [
                    "pc-i440fx-3.0",
                    "xenfv"
                ]
            }
            ```
        """
        ...
    @typing.overload
    def log_file_path(self, 
        id:'int',
    /) -> 'typing.Optional[str]': 
        """
        Retrieve log file path of `id` VM.
        
        It will return path of the log file if it exists and `null` otherwise.

        Parameters
        ----------
        id:
            Retrieve log file path of `id` VM.
        Returns
        -------
        typing.Optional[str]:
            log_file_path
        """
        ...
    @typing.overload
    def maximum_supported_vcpus(self, 
    /) -> 'int': 
        """
        Returns maximum supported VCPU's

        Parameters
        ----------
        Returns
        -------
        int:
            maximum_supported_vcpus
        """
        ...
    @typing.overload
    def port_wizard(self, 
    /) -> 'AvailableDisplayPort': 
        """
        It returns the next available Display Server Port and Web Port.
        
        Returns a dict with two keys `port` and `web`.

        Parameters
        ----------
        Returns
        -------
        AvailableDisplayPort:
            available_display_port
        """
        ...
    @typing.overload
    def poweroff(self, 
        id:'int',
    /) -> None: 
        """
        Poweroff a VM.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        """
        ...
    @typing.overload
    def profiles(self, 
    /) -> 'dict[str]': 
        """
        Returns a dictionary of defaults for different VM guest types.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            profiles
        """
        ...
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'typing.Union[list[VmEntry], VmEntry_, int, VmEntry__]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[VmEntry], VmEntry_, int, VmEntry__]:
            
        """
        ...
    @typing.overload
    def random_mac(self, 
    /) -> 'str': 
        """
        Create a random mac address.
        
        Returns:
            str: with six groups of two hexadecimal digits

        Parameters
        ----------
        Returns
        -------
        str:
            mac
        """
        ...
    @typing.overload
    def resolution_choices(self, 
    /) -> 'ResolutionChoices': 
        """
        Retrieve supported resolution choices for VM Display devices.

        Parameters
        ----------
        Returns
        -------
        ResolutionChoices:
            resolution_choices
        """
        ...
    @typing.overload
    def restart(self, 
        id:'int',
    /) -> None: 
        """
        Restart a VM.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        """
        ...
    @typing.overload
    def resume(self, 
        id:'int',
    /) -> None: 
        """
        Resume suspended `id` VM.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        """
        ...
    @typing.overload
    def start(self, 
        id:'int',
        options:'Options_'={},
    /) -> None: 
        """
        Start a VM.
        
        options.overcommit defaults to false, meaning VMs are not allowed to
        start if there is not enough available memory to hold all configured VMs.
        If true, VM starts even if there is not enough memory for all configured VMs.
        
        Error codes:
        
            ENOMEM(12): not enough free memory to run the VM without overcommit

        Parameters
        ----------
        id:
            id
        options:
            options
        Returns
        -------
        """
        ...
    @typing.overload
    def status(self, 
        id:'int',
    /) -> 'VmStatus': 
        """
        Get the status of `id` VM.
        
        Returns a dict:
            - state, RUNNING / STOPPED / SUSPENDED
            - pid, process id if RUNNING

        Parameters
        ----------
        id:
            Get the status of `id` VM.
        Returns
        -------
        VmStatus:
            vm_status
        """
        ...
    @typing.overload
    def stop(self, 
        id:'int',
        options:'Options__'={},
    /) -> None: 
        """
        Stops a VM.
        
        For unresponsive guests who have exceeded the `shutdown_timeout` defined by the user and have become
        unresponsive, they required to be powered down using `vm.poweroff`. `vm.stop` is only going to send a
        shutdown signal to the guest and wait the desired `shutdown_timeout` value before tearing down guest vmemory.
        
        `force_after_timeout` when supplied, it will initiate poweroff for the VM forcing it to exit if it has
        not already stopped within the specified `shutdown_timeout`.

        Parameters
        ----------
        id:
            id
        options:
            options
        Returns
        -------
        """
        ...
    @typing.overload
    def supports_virtualization(self, 
    /) -> 'bool': 
        """
        Returns "true" if system supports virtualization, "false" otherwise

        Parameters
        ----------
        Returns
        -------
        bool:
            supports_virtualization
        """
        ...
    @typing.overload
    def suspend(self, 
        id:'int',
    /) -> None: 
        """
        Suspend `id` VM.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        vm_update:'VmUpdate'={},
    /) -> 'VmUpdateReturns': 
        """
        Update all information of a specific VM.
        
        `devices` is a list of virtualized hardware to attach to the virtual machine. If `devices` is not present,
        no change is made to devices. If either the device list order or data stored by the device changes when the
        attribute is passed, these actions are taken:
        
        1) If there is no device in the `devices` list which was previously attached to the VM, that device is
           removed from the virtual machine.
        2) Devices are updated in the `devices` list when they contain a valid `id` attribute that corresponds to
           an existing device.
        3) Devices that do not have an `id` attribute are created and attached to `id` VM.

        Parameters
        ----------
        id:
            1) If there is no device in the `devices` list which was previously attached to the VM, that device is
               removed from the virtual machine.
            2) Devices are updated in the `devices` list when they contain a valid `id` attribute that corresponds to
               an existing device.
            3) Devices that do not have an `id` attribute are created and attached to `id` VM.
            Create a Virtual Machine (VM).
        vm_update:
            vm_update
        Returns
        -------
        VmUpdateReturns:
            vm_update_returns
        """
        ...
    @typing.overload
    def virtualization_details(self, 
    /) -> 'VirtualizationDetails': 
        """
        Retrieve details if virtualization is supported on the system and in case why it's not supported if it isn't.

        Parameters
        ----------
        Returns
        -------
        VirtualizationDetails:
            virtualization_details
        """
        ...
    class UEFI(str,Enum):
        UEFI = 'UEFI'
        ...
    class UEFICSM(str,Enum):
        LegacyBIOS = 'Legacy BIOS'
        ...
    BootloaderOptions = typing.TypedDict('BootloaderOptions', {
            'UEFI':'UEFI',
            'UEFI_CSM':'UEFICSM',
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
    Status = typing.TypedDict('Status', {
            'state':'str',
            'pid':'typing.Optional[int]',
            'domain_state':'str',
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
    CpuFlags = typing.TypedDict('CpuFlags', {
            'intel_vmx':'bool',
            'unrestricted_guest':'bool',
            'amd_rvi':'bool',
            'amd_asids':'bool',
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
    VmDeviceEntry = typing.TypedDict('VmDeviceEntry', {
            'dtype':'Dtype',
            'vm':'int',
            'attributes':'dict[str]',
            'order':'typing.Optional[int]',
            'id':'int',
    })
    class Protocol(str,Enum):
        HTTP = 'HTTP'
        HTTPS = 'HTTPS'
        ...
    Options = typing.TypedDict('Options', {
            'protocol':'Protocol',
    })
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
    Status_ = typing.TypedDict('Status_', {
            'state':'str',
            'pid':'typing.Optional[int]',
            'domain_state':'str',
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
            'status':'Status_',
            'id':'int',
    })
    Status__ = typing.TypedDict('Status__', {
            'state':'str',
            'pid':'typing.Optional[int]',
            'domain_state':'str',
    })
    VmEntry_ = typing.TypedDict('VmEntry_', {
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
            'status':'Status__',
            'id':'int',
    })
    Status___ = typing.TypedDict('Status___', {
            'state':'str',
            'pid':'typing.Optional[int]',
            'domain_state':'str',
    })
    VmEntry__ = typing.TypedDict('VmEntry__', {
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
            'status':'Status___',
            'id':'int',
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
    Status____ = typing.TypedDict('Status____', {
            'state':'str',
            'pid':'typing.Optional[int]',
            'domain_state':'str',
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
            'status':'Status____',
            'id':'int',
    })
    VirtualizationDetails = typing.TypedDict('VirtualizationDetails', {
            'supported':'bool',
            'error':'typing.Optional[str]',
    })
