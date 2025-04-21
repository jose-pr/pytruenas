from pytruenas import Namespace as _NS 
class Keychaincredential(_NS):
    
    def create(
        keychain_credential_create,
    ) -> KeychaincredentialCreate:
        """Create a Keychain Credential.

The following `type`s are supported: * `SSH_KEY_PAIR` * `SSH_CREDENTIALS`"""
        ...
    def delete(
        id,
        options,
    ) -> KeychaincredentialDelete:
        """Delete Keychain Credential with specific `id`."""
        ...
    def generate_ssh_key_pair(
    ) -> KeychaincredentialGenerate_ssh_key_pair:
        """Generate a public/private key pair (useful for `SSH_KEY_PAIR` type)"""
        ...
    def get_instance(
        id,
        options,
    ) -> KeychaincredentialGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(
        filters,
        options,
    ) -> KeychaincredentialQuery:
        """"""
        ...
    def remote_ssh_host_key_scan(
        keychain_remote_ssh_host_key_scan,
    ) -> KeychaincredentialRemote_ssh_host_key_scan:
        """Discover a remote host key (useful for `SSH_CREDENTIALS`)"""
        ...
    def remote_ssh_semiautomatic_setup(
        data,
    ) -> KeychaincredentialRemote_ssh_semiautomatic_setup:
        """Perform semi-automatic SSH connection setup with other TrueNAS machine.

It creates an `SSH_CREDENTIALS` credential with specified `name` that can be used to connect to TrueNAS machine with specified `url` and temporary auth `token`. Other TrueNAS machine adds `private_key` to allowed `username`'s private keys. Other `SSH_CREDENTIALS` attributes such as `connect_timeout` can be specified as well."""
        ...
    def setup_ssh_connection(
        options,
    ) -> KeychaincredentialSetup_ssh_connection:
        """Creates an SSH Connection performing the following steps:

1) Generate SSH Key Pair if required 2) Set up SSH Credentials based on `setup_type`

In case (2) fails, it will be ensured that SSH Key Pair generated (if applicable) in the process is removed."""
        ...
    def update(
        id,
        keychain_credential_update,
    ) -> KeychaincredentialUpdate:
        """Update a Keychain Credential with specific `id`.

Please note that you can't change `type`. You must specify full `attributes` value."""
        ...
    def used_by(
        id,
    ) -> KeychaincredentialUsed_by:
        """Returns list of objects that use this credential."""
        ...
class KeychaincredentialCreate:
    ...
class KeychaincredentialDelete:
    ...
class KeychaincredentialGenerate_ssh_key_pair:
    ...
class KeychaincredentialGet_instance:
    ...
class KeychaincredentialQuery:
    ...
class KeychaincredentialRemote_ssh_host_key_scan:
    ...
class KeychaincredentialRemote_ssh_semiautomatic_setup:
    ...
class KeychaincredentialSetup_ssh_connection:
    ...
class KeychaincredentialUpdate:
    ...
class KeychaincredentialUsed_by:
    ... 