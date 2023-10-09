
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
class Ssh(ConfigMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ssh')

    SshEntry = typing.TypedDict('SshEntry', {
            'bindiface':'list[str]',
            'tcpport':'int',
            'password_login_groups':'list[str]',
            'passwordauth':'bool',
            'kerberosauth':'bool',
            'tcpfwd':'bool',
            'compression':'bool',
            'sftp_log_level':'str',
            'sftp_log_facility':'str',
            'weak_ciphers':'list[str]',
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
            'sftp_log_level':'str',
            'sftp_log_facility':'str',
            'weak_ciphers':'list[str]',
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
            'sftp_log_level':'str',
            'sftp_log_facility':'str',
            'weak_ciphers':'list[str]',
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
