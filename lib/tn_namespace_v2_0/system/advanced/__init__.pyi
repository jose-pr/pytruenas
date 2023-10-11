
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class SystemAdvanced(
    Namespace
    ):
    _namespace:typing.Literal['system.advanced']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def config(self, 
    /) -> 'SystemAdvancedEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        SystemAdvancedEntry:
            system_advanced_entry
        """
        ...
    @typing.overload
    def sed_global_password(self, 
    /) -> 'str': 
        """
        Returns configured global SED password.

        Parameters
        ----------
        Returns
        -------
        str:
            sed_global_password
        """
        ...
    @typing.overload
    def serial_port_choices(self, 
    /) -> 'dict[str]': 
        """
        Get available choices for `serialport`.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            serial_port_choices
        """
        ...
    @typing.overload
    def syslog_certificate_authority_choices(self, 
    /) -> 'dict[str]': 
        """
        Return choices of certificate authorities which can be used for `syslog_tls_certificate_authority`.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            Syslog Certificate Authority Choices
        """
        ...
    @typing.overload
    def syslog_certificate_choices(self, 
    /) -> 'dict[str]': 
        """
        Return choices of certificates which can be used for `syslog_tls_certificate`.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            Syslog Certificate Choices
        """
        ...
    @typing.overload
    def update(self, 
        _system_advanced_update:'SystemAdvancedUpdate',
    /) -> 'SystemAdvancedUpdateReturns': 
        """
        Update System Advanced Service Configuration.
        
        `consolemenu` should be disabled if the menu at console is not desired. It will default to standard login
        in the console if disabled.
        
        `autotune` when enabled executes autotune script which attempts to optimize the system based on the installed
        hardware.
        
        When `syslogserver` is defined, logs of `sysloglevel` or above are sent.
        
        `consolemsg` is a deprecated attribute and will be removed in further releases. Please, use `consolemsg`
        attribute in the `system.general` plugin.
        
        `isolated_gpu_pci_ids` is a list of PCI ids which are isolated from host system.

        Parameters
        ----------
        system_advanced_update:
            system_advanced_update
        Returns
        -------
        SystemAdvancedUpdateReturns:
            system_advanced_update_returns
        """
        ...
    @typing.overload
    def update_gpu_pci_ids(self, 
        _isolated_gpu_pci_ids:'list[str]',
    /) -> None: 
        """
        `isolated_gpu_pci_ids` is a list of PCI ids which are isolated from host system.

        Parameters
        ----------
        isolated_gpu_pci_ids:
            isolated_gpu_pci_ids
        Returns
        -------
        """
        ...
    class SedUser(str,Enum):
        USER = 'USER'
        MASTER = 'MASTER'
        ...
    class Serialspeed(str,Enum):
        _9600 = '9600'
        _19200 = '19200'
        _38400 = '38400'
        _57600 = '57600'
        _115200 = '115200'
        ...
    class SyslogTransport(str,Enum):
        UDP = 'UDP'
        TCP = 'TCP'
        TLS = 'TLS'
        ...
    class Sysloglevel(str,Enum):
        FEMERG = 'F_EMERG'
        FALERT = 'F_ALERT'
        FCRIT = 'F_CRIT'
        FERR = 'F_ERR'
        FWARNING = 'F_WARNING'
        FNOTICE = 'F_NOTICE'
        FINFO = 'F_INFO'
        FDEBUG = 'F_DEBUG'
        ...
    SystemAdvancedEntry = typing.TypedDict('SystemAdvancedEntry', {
            'advancedmode':'bool',
            'autotune':'bool',
            'kdump_enabled':'bool',
            'boot_scrub':'int',
            'consolemenu':'bool',
            'consolemsg':'bool',
            'debugkernel':'bool',
            'fqdn_syslog':'bool',
            'motd':'str',
            'powerdaemon':'bool',
            'serialconsole':'bool',
            'serialport':'str',
            'anonstats_token':'str',
            'serialspeed':'Serialspeed',
            'swapondrive':'int',
            'overprovision':'typing.Optional[int]',
            'traceback':'bool',
            'uploadcrash':'bool',
            'anonstats':'bool',
            'sed_user':'SedUser',
            'sysloglevel':'Sysloglevel',
            'syslogserver':'str',
            'syslog_transport':'SyslogTransport',
            'syslog_tls_certificate':'typing.Optional[int]',
            'syslog_tls_certificate_authority':'typing.Optional[int]',
            'isolated_gpu_pci_ids':'list[str]',
            'kernel_extra_options':'str',
            'id':'int',
    })
    SystemAdvancedUpdate = typing.TypedDict('SystemAdvancedUpdate', {
            'advancedmode':'bool',
            'autotune':'bool',
            'kdump_enabled':'bool',
            'boot_scrub':'int',
            'consolemenu':'bool',
            'consolemsg':'bool',
            'debugkernel':'bool',
            'fqdn_syslog':'bool',
            'motd':'str',
            'powerdaemon':'bool',
            'serialconsole':'bool',
            'serialport':'str',
            'serialspeed':'Serialspeed',
            'swapondrive':'int',
            'overprovision':'typing.Optional[int]',
            'traceback':'bool',
            'uploadcrash':'bool',
            'anonstats':'bool',
            'sed_user':'SedUser',
            'sysloglevel':'Sysloglevel',
            'syslogserver':'str',
            'syslog_transport':'SyslogTransport',
            'syslog_tls_certificate':'typing.Optional[int]',
            'syslog_tls_certificate_authority':'typing.Optional[int]',
            'isolated_gpu_pci_ids':'list[str]',
            'kernel_extra_options':'str',
            'sed_passwd':'str',
    })
    SystemAdvancedUpdateReturns = typing.TypedDict('SystemAdvancedUpdateReturns', {
            'advancedmode':'bool',
            'autotune':'bool',
            'kdump_enabled':'bool',
            'boot_scrub':'int',
            'consolemenu':'bool',
            'consolemsg':'bool',
            'debugkernel':'bool',
            'fqdn_syslog':'bool',
            'motd':'str',
            'powerdaemon':'bool',
            'serialconsole':'bool',
            'serialport':'str',
            'anonstats_token':'str',
            'serialspeed':'Serialspeed',
            'swapondrive':'int',
            'overprovision':'typing.Optional[int]',
            'traceback':'bool',
            'uploadcrash':'bool',
            'anonstats':'bool',
            'sed_user':'SedUser',
            'sysloglevel':'Sysloglevel',
            'syslogserver':'str',
            'syslog_transport':'SyslogTransport',
            'syslog_tls_certificate':'typing.Optional[int]',
            'syslog_tls_certificate_authority':'typing.Optional[int]',
            'isolated_gpu_pci_ids':'list[str]',
            'kernel_extra_options':'str',
            'id':'int',
    })
