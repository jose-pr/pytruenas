
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class System(
    Namespace
    ):
    _namespace:typing.Literal['system']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def boot_id(self, 
    /) -> 'str': 
        """
        Returns an unique boot identifier.
        
        It is supposed to be unique every system boot.

        Parameters
        ----------
        Returns
        -------
        str:
            system_boot_identifier
        """
        ...
    @typing.overload
    def build_time(self, 
    /) -> 'str': 
        """
        Retrieve build time of the system.

        Parameters
        ----------
        Returns
        -------
        str:
            system_build_time
        """
        ...
    @typing.overload
    def debug(self, 
    /) -> None: 
        """
        Download a debug file.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def environment(self, 
    /) -> 'ProductRunningEnvironment': 
        """
        Return environment in which product is running. Possible values:
        - DEFAULT
        - EC2

        Parameters
        ----------
        Returns
        -------
        ProductRunningEnvironment:
            product_running_environment
        """
        ...
    @typing.overload
    def feature_enabled(self, 
        feature:'Feature',
    /) -> 'bool': 
        """
        Returns whether the `feature` is enabled or not

        Parameters
        ----------
        feature:
            feature
        Returns
        -------
        bool:
            feature_enabled
        """
        ...
    @typing.overload
    def host_id(self, 
    /) -> 'str': 
        """
        Retrieve a hex string that is generated based
        on the contents of the `/etc/hostid` file. This
        is a permanent value that persists across
        reboots/upgrades and can be used as a unique
        identifier for the machine.

        Parameters
        ----------
        Returns
        -------
        str:
            system_host_identifier
        """
        ...
    @typing.overload
    def info(self, 
    /) -> 'SystemInfo': 
        """
        Returns basic system information.

        Parameters
        ----------
        Returns
        -------
        SystemInfo:
            system_info
        """
        ...
    @typing.overload
    def is_freenas(self, 
    /) -> 'bool': 
        """
        FreeNAS is now TrueNAS CORE.
        
        DEPRECATED: Use `system.product_type`

        Parameters
        ----------
        Returns
        -------
        bool:
            system_is_truenas_core
        """
        ...
    @typing.overload
    def is_stable(self, 
    /) -> 'str': 
        """
        Returns whether software version of the system is stable.

        Parameters
        ----------
        Returns
        -------
        str:
            is_stable
        """
        ...
    @typing.overload
    def license_update(self, 
        license:'str',
    /) -> None: 
        """
        Update license file

        Parameters
        ----------
        license:
            license
        Returns
        -------
        """
        ...
    @typing.overload
    def product_name(self, 
    /) -> 'str': 
        """
        Returns name of the product we are using.

        Parameters
        ----------
        Returns
        -------
        str:
            product_name
        """
        ...
    @typing.overload
    def product_type(self, 
    /) -> 'str': 
        """
        Returns the type of the product.
        
        SCALE - TrueNAS SCALE, community version
        SCALE_ENTERPRISE - TrueNAS SCALE Enterprise, appliance version

        Parameters
        ----------
        Returns
        -------
        str:
            product_type
        """
        ...
    @typing.overload
    def ready(self, 
    /) -> 'bool': 
        """
        Returns whether the system completed boot and is ready to use

        Parameters
        ----------
        Returns
        -------
        bool:
            system_ready
        """
        ...
    @typing.overload
    def reboot(self, 
        system_reboot:'SystemReboot',
    /) -> None: 
        """
        Reboots the operating system.
        
        Emits an "added" event of name "system" and id "reboot".

        Parameters
        ----------
        system_reboot:
            system-reboot
        Returns
        -------
        """
        ...
    @typing.overload
    def release_notes_url(self, 
        version_str:'str',
    /) -> 'typing.Optional[str]': 
        """
        Returns the release notes URL for a version of SCALE.
        
        `version_str` str: represents a version to check against
        
        If `version` is not provided, then the release notes URL will return
            a link for the currently installed version of SCALE.

        Parameters
        ----------
        version_str:
            `version_str` str: represents a version to check against
        Returns
        -------
        typing.Optional[str]:
            truenas_release_notes_url
        """
        ...
    @typing.overload
    def shutdown(self, 
        system_shutdown:'SystemShutdown',
    /) -> None: 
        """
        Shuts down the operating system.
        
        An "added" event of name "system" and id "shutdown" is emitted when shutdown is initiated.

        Parameters
        ----------
        system_shutdown:
            system-shutdown
        Returns
        -------
        """
        ...
    @typing.overload
    def state(self, 
    /) -> 'SystemState': 
        """
        Returns system state:
        "BOOTING" - System is booting
        "READY" - System completed boot and is ready to use
        "SHUTTING_DOWN" - System is shutting down

        Parameters
        ----------
        Returns
        -------
        SystemState:
            system_state
        """
        ...
    @typing.overload
    def version(self, 
    /) -> 'str': 
        """
        Returns the full name of the software version of the system.

        Parameters
        ----------
        Returns
        -------
        str:
            truenas_version
        """
        ...
    @typing.overload
    def version_short(self, 
    /) -> 'str': 
        """
        Returns the short name of the software version of the system.

        Parameters
        ----------
        Returns
        -------
        str:
            truenas_version_shortname
        """
        ...
    class Feature(str,Enum):
        DEDUP = 'DEDUP'
        FIBRECHANNEL = 'FIBRECHANNEL'
        VM = 'VM'
        ...
    class ProductRunningEnvironment(str,Enum):
        DEFAULT = 'DEFAULT'
        EC2 = 'EC2'
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
