
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
from enum import Enum

class Ssh(ConfigMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ssh')

    class Cipher(str,Enum):
        AES128CBC = 'AES128-CBC'
        NONE = 'NONE'
        ...
    class SftpLogFacility(str,Enum):
        _ = ''
        DAEMON = 'DAEMON'
        USER = 'USER'
        AUTH = 'AUTH'
        LOCAL0 = 'LOCAL0'
        LOCAL1 = 'LOCAL1'
        LOCAL2 = 'LOCAL2'
        LOCAL3 = 'LOCAL3'
        LOCAL4 = 'LOCAL4'
        LOCAL5 = 'LOCAL5'
        LOCAL6 = 'LOCAL6'
        LOCAL7 = 'LOCAL7'
        ...
    class SftpLogLevel(str,Enum):
        _ = ''
        QUIET = 'QUIET'
        FATAL = 'FATAL'
        ERROR = 'ERROR'
        INFO = 'INFO'
        VERBOSE = 'VERBOSE'
        DEBUG = 'DEBUG'
        DEBUG2 = 'DEBUG2'
        DEBUG3 = 'DEBUG3'
        ...
    SshEntry = typing.TypedDict('SshEntry', {
            'bindiface':'list[str]',
            'tcpport':'int',
            'password_login_groups':'list[str]',
            'passwordauth':'bool',
            'kerberosauth':'bool',
            'tcpfwd':'bool',
            'compression':'bool',
            'sftp_log_level':'SftpLogLevel',
            'sftp_log_facility':'SftpLogFacility',
            'weak_ciphers':'list[Cipher]',
            'options':'str',
            'privatekey':'str',
            'host_dsa_key':'typing.Optional[str]',
            'host_dsa_key_pub':'typing.Optional[str]',
            'host_dsa_key_cert_pub':'typing.Optional[str]',
            'host_ecdsa_key':'typing.Optional[str]',
            'host_ecdsa_key_pub':'typing.Optional[str]',
            'host_ecdsa_key_cert_pub':'typing.Optional[str]',
            'host_ed25519_key':'typing.Optional[str]',
            'host_ed25519_key_pub':'typing.Optional[str]',
            'host_ed25519_key_cert_pub':'typing.Optional[str]',
            'host_key':'typing.Optional[str]',
            'host_key_pub':'typing.Optional[str]',
            'host_rsa_key':'typing.Optional[str]',
            'host_rsa_key_pub':'typing.Optional[str]',
            'host_rsa_key_cert_pub':'typing.Optional[str]',
            'id':'int',
    })
    SshUpdate = typing.TypedDict('SshUpdate', {
            'bindiface':'list[str]',
            'tcpport':'int',
            'password_login_groups':'list[str]',
            'passwordauth':'bool',
            'kerberosauth':'bool',
            'tcpfwd':'bool',
            'compression':'bool',
            'sftp_log_level':'SftpLogLevel',
            'sftp_log_facility':'SftpLogFacility',
            'weak_ciphers':'list[Cipher]',
            'options':'str',
    })
    SshUpdateReturns = typing.TypedDict('SshUpdateReturns', {
            'bindiface':'list[str]',
            'tcpport':'int',
            'password_login_groups':'list[str]',
            'passwordauth':'bool',
            'kerberosauth':'bool',
            'tcpfwd':'bool',
            'compression':'bool',
            'sftp_log_level':'SftpLogLevel',
            'sftp_log_facility':'SftpLogFacility',
            'weak_ciphers':'list[Cipher]',
            'options':'str',
            'privatekey':'str',
            'host_dsa_key':'typing.Optional[str]',
            'host_dsa_key_pub':'typing.Optional[str]',
            'host_dsa_key_cert_pub':'typing.Optional[str]',
            'host_ecdsa_key':'typing.Optional[str]',
            'host_ecdsa_key_pub':'typing.Optional[str]',
            'host_ecdsa_key_cert_pub':'typing.Optional[str]',
            'host_ed25519_key':'typing.Optional[str]',
            'host_ed25519_key_pub':'typing.Optional[str]',
            'host_ed25519_key_cert_pub':'typing.Optional[str]',
            'host_key':'typing.Optional[str]',
            'host_key_pub':'typing.Optional[str]',
            'host_rsa_key':'typing.Optional[str]',
            'host_rsa_key_pub':'typing.Optional[str]',
            'host_rsa_key_cert_pub':'typing.Optional[str]',
            'id':'int',
    })
