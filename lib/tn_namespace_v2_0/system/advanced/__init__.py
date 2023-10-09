
from pytruenas.base import Namespace

import typing
class SystemAdvanced(Namespace):
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
            'serialspeed':'str',
            'swapondrive':'int',
            'overprovision':'typing.Optional[int]',
            'traceback':'bool',
            'uploadcrash':'bool',
            'anonstats':'bool',
            'sed_user':'str',
            'sysloglevel':'str',
            'syslogserver':'str',
            'syslog_transport':'str',
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
            'serialspeed':'str',
            'swapondrive':'int',
            'overprovision':'typing.Optional[int]',
            'traceback':'bool',
            'uploadcrash':'bool',
            'anonstats':'bool',
            'sed_user':'str',
            'sysloglevel':'str',
            'syslogserver':'str',
            'syslog_transport':'str',
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
            'serialspeed':'str',
            'swapondrive':'int',
            'overprovision':'typing.Optional[int]',
            'traceback':'bool',
            'uploadcrash':'bool',
            'anonstats':'bool',
            'sed_user':'str',
            'sysloglevel':'str',
            'syslogserver':'str',
            'syslog_transport':'str',
            'syslog_tls_certificate':'typing.Optional[int]',
            'syslog_tls_certificate_authority':'typing.Optional[int]',
            'isolated_gpu_pci_ids':'list[str]',
            'kernel_extra_options':'str',
            'id':'int',
    })
