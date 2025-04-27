from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Ftp(_NS):
    
    def _update(self,
        __selector:_jsonschema.JsonValue=None,
        **fields:_ty.Unpack[FtpUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def config(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ConfigReturn:
        """"""
        ...
    def update(self,
        ftp_update:UpdateFtpUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update ftp service configuration.

`clients` is an integer value which sets the maximum number of simultaneous clients allowed. It defaults to 32.

`ipconnections` is an integer value which shows the maximum number of connections per IP address. It defaults to 0 which equals to unlimited.

`timeout` is the maximum number of seconds that proftpd will allow clients to stay connected without receiving any data on either the control or data connection.

`timeout_notransfer` is the maximum number of seconds a client is allowed to spend connected, after authentication, without issuing a command which results in creating an active or passive data connection (i.e. sending/receiving a file, or receiving a directory listing).

`onlyanonymous` allows anonymous FTP logins with access to the directory specified by `anonpath`.

`banner` is a message displayed to local login users after they successfully authenticate. It is not displayed to anonymous login users.

`filemask` sets the default permissions for newly created files which by default are 077.

`dirmask` sets the default permissions for newly created directories which by default are 077.

`resume` if set allows FTP clients to resume interrupted transfers.

`fxp` if set to true indicates that File eXchange Protocol is enabled. Generally it is discouraged as it makes the server vulnerable to FTP bounce attacks.

`defaultroot` when set ensures that for local users, home directory access is only granted if the user is a member of group wheel.

`ident` is a boolean value which when set to true indicates that IDENT authentication is required. If identd is not running on the client, this can result in timeouts.

`masqaddress` is the public IP address or hostname which is set if FTP clients cannot connect through a NAT device.

`localuserbw` is a positive integer value which indicates maximum upload bandwidth in KB/s for local user. Default of zero indicates unlimited upload bandwidth ( from the FTP server configuration ).

`localuserdlbw` is a positive integer value which indicates maximum download bandwidth in KB/s for local user. Default of zero indicates unlimited download bandwidth ( from the FTP server configuration ).

`anonuserbw` is a positive integer value which indicates maximum upload bandwidth in KB/s for anonymous user. Default of zero indicates unlimited upload bandwidth ( from the FTP server configuration ).

`anonuserdlbw` is a positive integer value which indicates maximum download bandwidth in KB/s for anonymous user. Default of zero indicates unlimited download bandwidth ( from the FTP server configuration ).

`tls` is a boolean value which when set indicates that encrypted connections are enabled. This requires a certificate to be configured first with the certificate service and the id of certificate is passed on in `ssltls_certificate`.

`tls_policy` defines whether the control channel, data channel, both channels, or neither channel of an FTP session must occur over SSL/TLS.

`tls_opt_enable_diags` is a boolean value when set, logs verbosely. This is helpful when troubleshooting a connection.

`options` is a string used to add proftpd(8) parameters not covered by ftp service."""
        ...
FtpUpdate = _ty.TypedDict('FtpUpdate', {
    'port': _ty.NotRequired[int],
    'clients': _ty.NotRequired[int],
    'ipconnections': _ty.NotRequired[int],
    'loginattempt': _ty.NotRequired[int],
    'timeout': _ty.NotRequired[int],
    'timeout_notransfer': _ty.NotRequired[int],
    'onlyanonymous': _ty.NotRequired[bool],
    'anonpath': _ty.NotRequired[str|None],
    'onlylocal': _ty.NotRequired[bool],
    'banner': _ty.NotRequired[str],
    'filemask': _ty.NotRequired[str],
    'dirmask': _ty.NotRequired[str],
    'fxp': _ty.NotRequired[bool],
    'resume': _ty.NotRequired[bool],
    'defaultroot': _ty.NotRequired[bool],
    'ident': _ty.NotRequired[bool],
    'reversedns': _ty.NotRequired[bool],
    'masqaddress': _ty.NotRequired[str],
    'passiveportsmin': _ty.NotRequired[int],
    'passiveportsmax': _ty.NotRequired[int],
    'localuserbw': _ty.NotRequired[int],
    'localuserdlbw': _ty.NotRequired[int],
    'anonuserbw': _ty.NotRequired[int],
    'anonuserdlbw': _ty.NotRequired[int],
    'tls': _ty.NotRequired[bool],
    'tls_policy': _ty.NotRequired[str],
    'tls_opt_allow_client_renegotiations': _ty.NotRequired[bool],
    'tls_opt_allow_dot_login': _ty.NotRequired[bool],
    'tls_opt_allow_per_user': _ty.NotRequired[bool],
    'tls_opt_common_name_required': _ty.NotRequired[bool],
    'tls_opt_enable_diags': _ty.NotRequired[bool],
    'tls_opt_export_cert_data': _ty.NotRequired[bool],
    'tls_opt_no_empty_fragments': _ty.NotRequired[bool],
    'tls_opt_no_session_reuse_required': _ty.NotRequired[bool],
    'tls_opt_stdenvvars': _ty.NotRequired[bool],
    'tls_opt_dns_name_required': _ty.NotRequired[bool],
    'tls_opt_ip_address_required': _ty.NotRequired[bool],
    'ssltls_certificate': _ty.NotRequired[int|None],
    'options': _ty.NotRequired[str], 
})
ConfigReturn = _ty.TypedDict('ConfigReturn', {
    'id': int,
    'port': int,
    'clients': int,
    'ipconnections': int,
    'loginattempt': int,
    'timeout': int,
    'timeout_notransfer': int,
    'onlyanonymous': bool,
    'anonpath': str|None,
    'onlylocal': bool,
    'banner': str,
    'filemask': str,
    'dirmask': str,
    'fxp': bool,
    'resume': bool,
    'defaultroot': bool,
    'ident': bool,
    'reversedns': bool,
    'masqaddress': str,
    'passiveportsmin': int,
    'passiveportsmax': int,
    'localuserbw': int,
    'localuserdlbw': int,
    'anonuserbw': int,
    'anonuserdlbw': int,
    'tls': bool,
    'tls_policy': str,
    'tls_opt_allow_client_renegotiations': bool,
    'tls_opt_allow_dot_login': bool,
    'tls_opt_allow_per_user': bool,
    'tls_opt_common_name_required': bool,
    'tls_opt_enable_diags': bool,
    'tls_opt_export_cert_data': bool,
    'tls_opt_no_empty_fragments': bool,
    'tls_opt_no_session_reuse_required': bool,
    'tls_opt_stdenvvars': bool,
    'tls_opt_dns_name_required': bool,
    'tls_opt_ip_address_required': bool,
    'ssltls_certificate': int|None,
    'options': str, 
})
UpdateFtpUpdate = _ty.TypedDict('UpdateFtpUpdate', {
    'port': _ty.NotRequired[int],
    'clients': _ty.NotRequired[int],
    'ipconnections': _ty.NotRequired[int],
    'loginattempt': _ty.NotRequired[int],
    'timeout': _ty.NotRequired[int],
    'timeout_notransfer': _ty.NotRequired[int],
    'onlyanonymous': _ty.NotRequired[bool],
    'anonpath': _ty.NotRequired[str|None],
    'onlylocal': _ty.NotRequired[bool],
    'banner': _ty.NotRequired[str],
    'filemask': _ty.NotRequired[str],
    'dirmask': _ty.NotRequired[str],
    'fxp': _ty.NotRequired[bool],
    'resume': _ty.NotRequired[bool],
    'defaultroot': _ty.NotRequired[bool],
    'ident': _ty.NotRequired[bool],
    'reversedns': _ty.NotRequired[bool],
    'masqaddress': _ty.NotRequired[str],
    'passiveportsmin': _ty.NotRequired[int],
    'passiveportsmax': _ty.NotRequired[int],
    'localuserbw': _ty.NotRequired[int],
    'localuserdlbw': _ty.NotRequired[int],
    'anonuserbw': _ty.NotRequired[int],
    'anonuserdlbw': _ty.NotRequired[int],
    'tls': _ty.NotRequired[bool],
    'tls_policy': _ty.NotRequired[str],
    'tls_opt_allow_client_renegotiations': _ty.NotRequired[bool],
    'tls_opt_allow_dot_login': _ty.NotRequired[bool],
    'tls_opt_allow_per_user': _ty.NotRequired[bool],
    'tls_opt_common_name_required': _ty.NotRequired[bool],
    'tls_opt_enable_diags': _ty.NotRequired[bool],
    'tls_opt_export_cert_data': _ty.NotRequired[bool],
    'tls_opt_no_empty_fragments': _ty.NotRequired[bool],
    'tls_opt_no_session_reuse_required': _ty.NotRequired[bool],
    'tls_opt_stdenvvars': _ty.NotRequired[bool],
    'tls_opt_dns_name_required': _ty.NotRequired[bool],
    'tls_opt_ip_address_required': _ty.NotRequired[bool],
    'ssltls_certificate': _ty.NotRequired[int|None],
    'options': _ty.NotRequired[str], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'port': int,
    'clients': int,
    'ipconnections': int,
    'loginattempt': int,
    'timeout': int,
    'timeout_notransfer': int,
    'onlyanonymous': bool,
    'anonpath': str|None,
    'onlylocal': bool,
    'banner': str,
    'filemask': str,
    'dirmask': str,
    'fxp': bool,
    'resume': bool,
    'defaultroot': bool,
    'ident': bool,
    'reversedns': bool,
    'masqaddress': str,
    'passiveportsmin': int,
    'passiveportsmax': int,
    'localuserbw': int,
    'localuserdlbw': int,
    'anonuserbw': int,
    'anonuserdlbw': int,
    'tls': bool,
    'tls_policy': str,
    'tls_opt_allow_client_renegotiations': bool,
    'tls_opt_allow_dot_login': bool,
    'tls_opt_allow_per_user': bool,
    'tls_opt_common_name_required': bool,
    'tls_opt_enable_diags': bool,
    'tls_opt_export_cert_data': bool,
    'tls_opt_no_empty_fragments': bool,
    'tls_opt_no_session_reuse_required': bool,
    'tls_opt_stdenvvars': bool,
    'tls_opt_dns_name_required': bool,
    'tls_opt_ip_address_required': bool,
    'ssltls_certificate': int|None,
    'options': str, 
})