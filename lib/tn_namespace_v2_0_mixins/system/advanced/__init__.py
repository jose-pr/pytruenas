
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
from enum import Enum

class SystemAdvanced(ConfigMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'system.advanced')

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
    class Serialspeed(str,Enum):
        _9600 = '9600'
        _19200 = '19200'
        _38400 = '38400'
        _57600 = '57600'
        _115200 = '115200'
        ...
    class SedUser(str,Enum):
        USER = 'USER'
        MASTER = 'MASTER'
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
    class SyslogTransport(str,Enum):
        UDP = 'UDP'
        TCP = 'TCP'
        TLS = 'TLS'
        ...
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
