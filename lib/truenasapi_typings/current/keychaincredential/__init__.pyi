from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Keychaincredential(_NS):
    
    def _create(self,
        **fields:_ty.Unpack[KeychainCredentialCreateSSHKeyPairEntry|KeychainCredentialCreateSSHCredentialsEntry],
    ) -> CreateReturn:
        """"""
        ...
    def _get(self,
        __id_or_filter:int|_ty.Sequence[str]|None=None,
        **fields:_ty.Unpack[Get],
    ) -> GetInstanceReturn|None:
        """"""
        ...
    def _update(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[KeychainCredentialUpdateSSHKeyPairEntry|KeychainCredentialUpdateSSHCredentialsEntry],
    ) -> UpdateReturn:
        """"""
        ...
    def _upsert(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[KeychainCredentialUpdateSSHKeyPairEntry|KeychainCredentialUpdateSSHCredentialsEntry],
    ) -> UpdateReturn:
        """"""
        ...
    def create(self,
        keychain_credential_create:CreateKeychainCredentialCreateSSHKeyPairEntry|CreateKeychainCredentialCreateSSHCredentialsEntry,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateSSHKeyPairEntry|CreateSSHCredentialsEntry:
        """Create a Keychain Credential.

The following `type`s are supported: * `SSH_KEY_PAIR` * `SSH_CREDENTIALS`"""
        ...
    def delete(self,
        id:int,
        options:DeleteOptions={'cascade': False},
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
    ) -> GenerateSshKeyPairReturn:
        """Generate a public/private key pair (useful for `SSH_KEY_PAIR` type)"""
        ...
    def get_instance(self,
        id:int,
        options:GetInstanceOptions={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GetInstanceReturn:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:QueryOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[QueryKeychainCredentialQueryResultItem]|QueryKeychainCredentialQueryResultItem|int:
        """"""
        ...
    def remote_ssh_host_key_scan(self,
        keychain_remote_ssh_host_key_scan:RemoteSshHostKeyScanKeychainRemoteSshHostKeyScan,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> str:
        """Discover a remote host key (useful for `SSH_CREDENTIALS`)"""
        ...
    def remote_ssh_semiautomatic_setup(self,
        data:RemoteSshSemiautomaticSetupData,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> RemoteSshSemiautomaticSetupReturn:
        """Perform semi-automatic SSH connection setup with other TrueNAS machine.

It creates an `SSH_CREDENTIALS` credential with specified `name` that can be used to connect to TrueNAS machine with specified `url` and temporary auth `token`. Other TrueNAS machine adds `private_key` to allowed `username`'s private keys. Other `SSH_CREDENTIALS` attributes such as `connect_timeout` can be specified as well."""
        ...
    def setup_ssh_connection(self,
        options:SetupSshConnectionSetupSSHConnectionManual|SetupSshConnectionSetupSSHConnectionSemiautomatic,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SetupSshConnectionReturn:
        """Creates an SSH Connection performing the following steps:

1) Generate SSH Key Pair if required 2) Set up SSH Credentials based on `setup_type`

In case (2) fails, it will be ensured that SSH Key Pair generated (if applicable) in the process is removed."""
        ...
    def update(self,
        id:int,
        keychain_credential_update:UpdateKeychainCredentialUpdateSSHKeyPairEntry|UpdateKeychainCredentialUpdateSSHCredentialsEntry,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateSSHKeyPairEntry|UpdateSSHCredentialsEntry:
        """Update a Keychain Credential with specific `id`.

Please note that you can't change `type`. You must specify full `attributes` value."""
        ...
    def used_by(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[UsedByUsedKeychainCredential]:
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
Get = _ty.TypedDict('Get', {
    'id': _ty.NotRequired[int],
    'name': _ty.NotRequired[str],
    'type': _ty.NotRequired[str],
    'attributes': _ty.NotRequired[_jsonschema.JsonValue|_jsonschema.JsonValue], 
})
KeychainCredentialUpdateSSHKeyPairEntry = _ty.TypedDict('KeychainCredentialUpdateSSHKeyPairEntry', {
    'name': _ty.NotRequired[str],
    'attributes': _ty.NotRequired[_jsonschema.JsonValue], 
})
KeychainCredentialUpdateSSHCredentialsEntry = _ty.TypedDict('KeychainCredentialUpdateSSHCredentialsEntry', {
    'name': _ty.NotRequired[str],
    'attributes': _ty.NotRequired[_jsonschema.JsonValue], 
})
CreateKeychainCredentialCreateSSHKeyPairEntry = _ty.TypedDict('CreateKeychainCredentialCreateSSHKeyPairEntry', {
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonValue, 
})
CreateKeychainCredentialCreateSSHCredentialsEntry = _ty.TypedDict('CreateKeychainCredentialCreateSSHCredentialsEntry', {
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonValue, 
})
CreateSSHKeyPairEntry = _ty.TypedDict('CreateSSHKeyPairEntry', {
    'id': int,
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonValue, 
})
CreateSSHCredentialsEntry = _ty.TypedDict('CreateSSHCredentialsEntry', {
    'id': int,
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonValue, 
})
DeleteOptions = _ty.TypedDict('DeleteOptions', {
    'cascade': _ty.NotRequired[bool], 
})
GenerateSshKeyPairReturn = _ty.TypedDict('GenerateSshKeyPairReturn', {
    'private_key': str,
    'public_key': str, 
})
GetInstanceOptions = _ty.TypedDict('GetInstanceOptions', {
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
GetInstanceReturn = _ty.TypedDict('GetInstanceReturn', {
    'id': int,
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonValue|_jsonschema.JsonValue, 
})
QueryOptions = _ty.TypedDict('QueryOptions', {
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
QueryKeychainCredentialQueryResultItem = _ty.TypedDict('QueryKeychainCredentialQueryResultItem', {
    'id': _ty.NotRequired[int],
    'name': _ty.NotRequired[str],
    'type': _ty.NotRequired[str],
    'attributes': _ty.NotRequired[_jsonschema.JsonValue|_jsonschema.JsonValue], 
})
RemoteSshHostKeyScanKeychainRemoteSshHostKeyScan = _ty.TypedDict('RemoteSshHostKeyScanKeychainRemoteSshHostKeyScan', {
    'host': str,
    'port': _ty.NotRequired[int],
    'connect_timeout': _ty.NotRequired[int], 
})
RemoteSshSemiautomaticSetupData = _ty.TypedDict('RemoteSshSemiautomaticSetupData', {
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
RemoteSshSemiautomaticSetupReturn = _ty.TypedDict('RemoteSshSemiautomaticSetupReturn', {
    'id': int,
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonValue, 
})
SetupSshConnectionSetupSSHConnectionManual = _ty.TypedDict('SetupSshConnectionSetupSSHConnectionManual', {
    'private_key': _jsonschema.JsonValue|_jsonschema.JsonValue,
    'connection_name': str,
    'setup_type': _ty.NotRequired[str],
    'manual_setup': _jsonschema.JsonValue, 
})
SetupSshConnectionSetupSSHConnectionSemiautomatic = _ty.TypedDict('SetupSshConnectionSetupSSHConnectionSemiautomatic', {
    'private_key': _jsonschema.JsonValue|_jsonschema.JsonValue,
    'connection_name': str,
    'setup_type': _ty.NotRequired[str],
    'semi_automatic_setup': _jsonschema.JsonValue, 
})
SetupSshConnectionReturn = _ty.TypedDict('SetupSshConnectionReturn', {
    'id': int,
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonValue, 
})
UpdateKeychainCredentialUpdateSSHKeyPairEntry = _ty.TypedDict('UpdateKeychainCredentialUpdateSSHKeyPairEntry', {
    'name': _ty.NotRequired[str],
    'attributes': _ty.NotRequired[_jsonschema.JsonValue], 
})
UpdateKeychainCredentialUpdateSSHCredentialsEntry = _ty.TypedDict('UpdateKeychainCredentialUpdateSSHCredentialsEntry', {
    'name': _ty.NotRequired[str],
    'attributes': _ty.NotRequired[_jsonschema.JsonValue], 
})
UpdateSSHKeyPairEntry = _ty.TypedDict('UpdateSSHKeyPairEntry', {
    'id': int,
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonValue, 
})
UpdateSSHCredentialsEntry = _ty.TypedDict('UpdateSSHCredentialsEntry', {
    'id': int,
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonValue, 
})
UsedByUsedKeychainCredential = _ty.TypedDict('UsedByUsedKeychainCredential', {
    'title': str,
    'unbind_method': str, 
})