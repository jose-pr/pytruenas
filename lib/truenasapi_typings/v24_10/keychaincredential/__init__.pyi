from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Keychaincredential(_NS):
    
    def create(self,
        keychain_credential_create:KeychainCredentialCreateSSHKeyPairEntry|KeychainCredentialCreateSSHCredentialsEntry,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SSHKeyPairEntry|SSHCredentialsEntry:
        """Create a Keychain Credential.

The following `type`s are supported: * `SSH_KEY_PAIR` * `SSH_CREDENTIALS`"""
        ...
    def delete(self,
        id:int,
        options:options={'cascade': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Delete Keychain Credential with specific `id`."""
        ...
    def generate_ssh_key_pair(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> KeychaincredentialGenerate_ssh_key_pair:
        """Generate a public/private key pair (useful for `SSH_KEY_PAIR` type)"""
        ...
    def get_instance(self,
        id:int,
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> KeychaincredentialGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[KeychainCredentialQueryResultItem]|KeychainCredentialQueryResultItem|int:
        """"""
        ...
    def remote_ssh_host_key_scan(self,
        keychain_remote_ssh_host_key_scan:keychain_remote_ssh_host_key_scan,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> str:
        """Discover a remote host key (useful for `SSH_CREDENTIALS`)"""
        ...
    def remote_ssh_semiautomatic_setup(self,
        data:data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> KeychaincredentialRemote_ssh_semiautomatic_setup:
        """Perform semi-automatic SSH connection setup with other TrueNAS machine.

It creates an `SSH_CREDENTIALS` credential with specified `name` that can be used to connect to TrueNAS machine with specified `url` and temporary auth `token`. Other TrueNAS machine adds `private_key` to allowed `username`'s private keys. Other `SSH_CREDENTIALS` attributes such as `connect_timeout` can be specified as well."""
        ...
    def setup_ssh_connection(self,
        options:SetupSSHConnectionManual|SetupSSHConnectionSemiautomatic,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> KeychaincredentialSetup_ssh_connection:
        """Creates an SSH Connection performing the following steps:

1) Generate SSH Key Pair if required 2) Set up SSH Credentials based on `setup_type`

In case (2) fails, it will be ensured that SSH Key Pair generated (if applicable) in the process is removed."""
        ...
    def update(self,
        id:int,
        keychain_credential_update:KeychainCredentialUpdateSSHKeyPairEntry|KeychainCredentialUpdateSSHCredentialsEntry,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SSHKeyPairEntry|SSHCredentialsEntry:
        """Update a Keychain Credential with specific `id`.

Please note that you can't change `type`. You must specify full `attributes` value."""
        ...
    def used_by(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[UsedKeychainCredential]:
        """Returns list of objects that use this credential."""
        ...
KeychainCredentialCreateSSHKeyPairEntry = _ty.TypedDict('KeychainCredentialCreateSSHKeyPairEntry', {
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonValue, 
})
KeychainCredentialCreateSSHCredentialsEntry = _ty.TypedDict('KeychainCredentialCreateSSHCredentialsEntry', {
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonValue, 
})
SSHKeyPairEntry = _ty.TypedDict('SSHKeyPairEntry', {
    'id': int,
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonValue, 
})
SSHCredentialsEntry = _ty.TypedDict('SSHCredentialsEntry', {
    'id': int,
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonValue, 
})
options = _ty.TypedDict('options', {
    'relationships': _ty.NotRequired[bool],
    'extend': _ty.NotRequired[str|None],
    'extend_context': _ty.NotRequired[str|None],
    'prefix': _ty.NotRequired[str|None],
    'extra': _ty.NotRequired[_jsonschema.JsonObject],
    'order_by': _ty.NotRequired[list[str]],
    'select': _ty.NotRequired[list[str|_jsonschema.JsonArray]],
    'count': _ty.NotRequired[bool],
    'get': _ty.NotRequired[bool],
    'offset': _ty.NotRequired[int],
    'limit': _ty.NotRequired[int],
    'force_sql_filters': _ty.NotRequired[bool], 
})
KeychaincredentialGenerate_ssh_key_pair = _ty.TypedDict('KeychaincredentialGenerate_ssh_key_pair', {
    'private_key': str,
    'public_key': str, 
})
KeychaincredentialGet_instance = _ty.TypedDict('KeychaincredentialGet_instance', {
    'id': int,
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonValue|_jsonschema.JsonValue, 
})
KeychainCredentialQueryResultItem = _ty.TypedDict('KeychainCredentialQueryResultItem', {
    'id': _ty.NotRequired[int],
    'name': _ty.NotRequired[str],
    'type': _ty.NotRequired[str],
    'attributes': _ty.NotRequired[_jsonschema.JsonValue|_jsonschema.JsonValue], 
})
keychain_remote_ssh_host_key_scan = _ty.TypedDict('keychain_remote_ssh_host_key_scan', {
    'host': str,
    'port': _ty.NotRequired[int],
    'connect_timeout': _ty.NotRequired[int], 
})
data = _ty.TypedDict('data', {
    'name': str,
    'url': str,
    'verify_ssl': _ty.NotRequired[bool],
    'token': _ty.NotRequired[str|None],
    'admin_username': _ty.NotRequired[str],
    'password': _ty.NotRequired[str|None],
    'otp_token': _ty.NotRequired[str|None],
    'username': _ty.NotRequired[str],
    'private_key': int,
    'connect_timeout': _ty.NotRequired[int],
    'sudo': _ty.NotRequired[bool], 
})
KeychaincredentialRemote_ssh_semiautomatic_setup = _ty.TypedDict('KeychaincredentialRemote_ssh_semiautomatic_setup', {
    'id': int,
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonValue, 
})
SetupSSHConnectionManual = _ty.TypedDict('SetupSSHConnectionManual', {
    'private_key': _jsonschema.JsonValue|_jsonschema.JsonValue,
    'connection_name': str,
    'setup_type': _ty.NotRequired[str],
    'manual_setup': _jsonschema.JsonValue, 
})
SetupSSHConnectionSemiautomatic = _ty.TypedDict('SetupSSHConnectionSemiautomatic', {
    'private_key': _jsonschema.JsonValue|_jsonschema.JsonValue,
    'connection_name': str,
    'setup_type': _ty.NotRequired[str],
    'semi_automatic_setup': _jsonschema.JsonValue, 
})
KeychaincredentialSetup_ssh_connection = _ty.TypedDict('KeychaincredentialSetup_ssh_connection', {
    'id': int,
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonValue, 
})
KeychainCredentialUpdateSSHKeyPairEntry = _ty.TypedDict('KeychainCredentialUpdateSSHKeyPairEntry', {
    'name': _ty.NotRequired[str],
    'attributes': _ty.NotRequired[_jsonschema.JsonValue], 
})
KeychainCredentialUpdateSSHCredentialsEntry = _ty.TypedDict('KeychainCredentialUpdateSSHCredentialsEntry', {
    'name': _ty.NotRequired[str],
    'attributes': _ty.NotRequired[_jsonschema.JsonValue], 
})
UsedKeychainCredential = _ty.TypedDict('UsedKeychainCredential', {
    'title': str,
    'unbind_method': str, 
})