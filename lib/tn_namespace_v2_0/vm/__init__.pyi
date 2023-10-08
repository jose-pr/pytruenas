
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Vm(Namespace):
    _namespace:_ty.Literal['vm']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def bootloader_options(self, 
    /) -> 'dict[str]': 
        """
        Supported motherboard firmware options.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            bootloader_options
        """
        ...
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
    def create(self, 
        vm_create:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            vm_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
        vm_delete:'dict[str]'={},
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
    @_ty.overload
    def flags(self, 
    /) -> 'dict[str]': 
        """
        Returns a dictionary with CPU flags for the hypervisor.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            cpu_flags
        """
        ...
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
    def get_display_devices(self, 
        id:'int',
    /) -> 'list': 
        """
        Get the display devices from a given guest. If a display device has password configured,
        `attributes.password_configured` will be set to `true`.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        list:
            get_display_devices
        """
        ...
    @_ty.overload
    def get_display_web_uri(self, 
        id:'int',
        host:'str'="",
        options:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            display_devices_uri
        """
        ...
    @_ty.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'dict[str]'={},
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
    @_ty.overload
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
    @_ty.overload
    def get_vm_memory_info(self, 
        vm_id:'int',
    /) -> 'dict[str]': 
        """
        Returns memory information for `vm_id` VM if it is going to be started.
        
        All memory attributes are expressed in bytes.

        Parameters
        ----------
        vm_id:
            Returns memory information for `vm_id` VM if it is going to be started.
        Returns
        -------
        dict[str]:
            get_vm_memory_info
        """
        ...
    @_ty.overload
    def get_vmemory_in_use(self, 
    /) -> 'dict[str]': 
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
        dict[str]:
            vmemory_in_use
        """
        ...
    @_ty.overload
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
    @_ty.overload
    def log_file_path(self, 
        id:'int',
    /) -> 'str|None': 
        """
        Retrieve log file path of `id` VM.
        
        It will return path of the log file if it exists and `null` otherwise.

        Parameters
        ----------
        id:
            Retrieve log file path of `id` VM.
        Returns
        -------
        str:
            log_file_path
        None:
            log_file_path
        """
        ...
    @_ty.overload
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
    @_ty.overload
    def port_wizard(self, 
    /) -> 'dict[str]': 
        """
        It returns the next available Display Server Port and Web Port.
        
        Returns a dict with two keys `port` and `web`.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            available_display_port
        """
        ...
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @_ty.overload
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
    @_ty.overload
    def resolution_choices(self, 
    /) -> 'dict[str]': 
        """
        Retrieve supported resolution choices for VM Display devices.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            resolution_choices
        """
        ...
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
    def start(self, 
        id:'int',
        options:'dict[str]'={},
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
    @_ty.overload
    def status(self, 
        id:'int',
    /) -> 'dict[str]': 
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
        dict[str]:
            vm_status
        """
        ...
    @_ty.overload
    def stop(self, 
        id:'int',
        options:'dict[str]'={},
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
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
    def update(self, 
        id:'int',
        vm_update:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            vm_update_returns
        """
        ...
    @_ty.overload
    def virtualization_details(self, 
    /) -> 'dict[str]': 
        """
        Retrieve details if virtualization is supported on the system and in case why it's not supported if it isn't.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            virtualization_details
        """
        ...
