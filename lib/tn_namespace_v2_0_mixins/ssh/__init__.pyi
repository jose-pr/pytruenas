
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
class Ssh(
    ConfigMixin,
    Namespace
    ):
    _namespace:typing.Literal['ssh']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def bindiface_choices(self, 
    /) -> 'dict[str]': 
        """
        Available choices for the bindiface attribute of SSH service.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            ssh_bind_interfaces_choices
        """
        ...
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
    @typing.overload
    def config(self, 
    /) -> 'SshEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        SshEntry:
            ssh_entry
        """
        ...
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
    @typing.overload
    def update(self, 
        ssh_update:'SshUpdate'={},
    /) -> 'SshUpdateReturns': 
        """
        Update settings of SSH daemon service.
        
        If `bindiface` is empty it will listen for all available addresses.

        Parameters
        ----------
        ssh_update:
            ssh_update
        Returns
        -------
        SshUpdateReturns:
            ssh_update_returns
        """
        ...
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

