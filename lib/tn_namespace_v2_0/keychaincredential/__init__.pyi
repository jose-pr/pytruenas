
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Keychaincredential(
    Namespace
    ):
    _namespace:typing.Literal['keychaincredential']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        keychain_credential_create:'KeychainCredentialCreate'={},
    /) -> 'KeychaincredentialCreateReturns': 
        """
        Create a Keychain Credential
        
        Create a Keychain Credential of any type.
        Every Keychain Credential has a `name` which is used to distinguish it from others.
        The following `type`s are supported:
         * `SSH_KEY_PAIR`
           Which `attributes` are:
           * `private_key`
           * `public_key` (which can be omitted and thus automatically derived from private key)
           At least one attribute is required.
        
         * `SSH_CREDENTIALS`
           Which `attributes` are:
           * `host`
           * `port` (default 22)
           * `username` (default root)
           * `private_key` (Keychain Credential ID)
           * `remote_host_key` (you can use `keychaincredential.remote_ssh_host_key_scan` do discover it)
           * `connect_timeout` (default 10)

        Parameters
        ----------
        keychain_credential_create:
            keychain_credential_create
        Returns
        -------
        KeychaincredentialCreateReturns:
            keychaincredential_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
        options:'Options'={},
    /) -> None: 
        """
        Delete Keychain Credential with specific `id`

        Parameters
        ----------
        id:
            Delete Keychain Credential with specific `id`
        options:
            options
        Returns
        -------
        """
        ...
    @typing.overload
    def generate_ssh_key_pair(self, 
    /) -> 'SshKeyPair': 
        """
        Generate a public/private key pair
        
        Generate a public/private key pair (useful for `SSH_KEY_PAIR` type)

        Parameters
        ----------
        Returns
        -------
        SshKeyPair:
            ssh_key_pair
        """
        ...
    @typing.overload
    def get_instance(self, 
        id:'typing.Union[str, int, bool, dict[str], list]',
        query_options_get_instance:'QueryOptionsGetInstance'={},
    /) -> None: 
        """
        Returns instance matching `id`. If `id` is not found, Validation error is raised.
        
        Please see `query` method documentation for `options`.

        Parameters
        ----------
        id:
            Returns instance matching `id`. If `id` is not found, Validation error is raised.
        query_options_get_instance:
            query-options-get_instance
        Returns
        -------
        """
        ...
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'typing.Union[list[KeychainCredentialEntry], KeychainCredentialEntry, int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[KeychainCredentialEntry], KeychainCredentialEntry, int]:
            
        """
        ...
    @typing.overload
    def remote_ssh_host_key_scan(self, 
        keychain_remote_ssh_host_key_scan:'KeychainRemoteSshHostKeyScan'={},
    /) -> 'str': 
        """
        Discover a remote host key
        
        Discover a remote host key (useful for `SSH_CREDENTIALS`)

        Parameters
        ----------
        keychain_remote_ssh_host_key_scan:
            keychain_remote_ssh_host_key_scan
        Returns
        -------
        str:
            remove_ssh_host_key
        """
        ...
    @typing.overload
    def remote_ssh_semiautomatic_setup(self, 
        keychain_remote_ssh_semiautomatic_setup:'KeychainRemoteSshSemiautomaticSetup'={},
    /) -> 'KeychainCredentialEntry': 
        """
        Perform semi-automatic SSH connection setup with other FreeNAS machine
        
        Perform semi-automatic SSH connection setup with other FreeNAS machine. It creates a `SSH_CREDENTIALS`
        credential with specified `name` that can be used to connect to FreeNAS machine with specified `url` and
        temporary auth `token`. Other FreeNAS machine adds `private_key` to allowed `username`'s private keys. Other
        `SSH_CREDENTIALS` attributes such as `connect_timeout` can be specified as well.

        Parameters
        ----------
        keychain_remote_ssh_semiautomatic_setup:
            keychain_remote_ssh_semiautomatic_setup
        Returns
        -------
        KeychainCredentialEntry:
            keychain_credential_entry
        """
        ...
    @typing.overload
    def setup_ssh_connection(self, 
        setup_ssh_connection:'SetupSshConnection'={},
    /) -> 'KeychainCredentialEntry': 
        """
        Creates a SSH Connection performing the following steps:
        
        1) Generating SSH Key Pair if required
        2) Setting up SSH Credentials based on `setup_type`
        
        In case (2) fails, it will be ensured that SSH Key Pair generated ( if applicable ) in the process is
        removed.

        Parameters
        ----------
        setup_ssh_connection:
            setup_ssh_connection
        Returns
        -------
        KeychainCredentialEntry:
            keychain_credential_entry
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        keychain_credential_update:'KeychainCredentialUpdate'={},
    /) -> 'KeychaincredentialUpdateReturns': 
        """
        Update a Keychain Credential with specific `id`
        
        Please note that you can't change `type`
        
        Also you must specify full `attributes` value
        
        See the documentation for `create` method for information on payload contents

        Parameters
        ----------
        id:
            Update a Keychain Credential with specific `id`
        keychain_credential_update:
            keychain_credential_update
        Returns
        -------
        KeychaincredentialUpdateReturns:
            keychaincredential_update_returns
        """
        ...
    @typing.overload
    def used_by(self, 
        id:'int',
    /) -> 'list[CredentialResult]': 
        """
        Returns list of objects that use this credential.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        list[CredentialResult]:
            credential_results
        """
        ...
    KeychainCredentialCreate = typing.TypedDict('KeychainCredentialCreate', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
    })
    KeychaincredentialCreateReturns = typing.TypedDict('KeychaincredentialCreateReturns', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'id':'int',
    })
    Options = typing.TypedDict('Options', {
            'cascade':'bool',
    })
    SshKeyPair = typing.TypedDict('SshKeyPair', {
            'private_key':'str',
            'public_key':'str',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    KeychainCredentialEntry = typing.TypedDict('KeychainCredentialEntry', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'id':'int',
    })
    KeychainRemoteSshHostKeyScan = typing.TypedDict('KeychainRemoteSshHostKeyScan', {
            'host':'str',
            'port':'str',
            'connect_timeout':'int',
    })
    KeychainRemoteSshSemiautomaticSetup = typing.TypedDict('KeychainRemoteSshSemiautomaticSetup', {
            'name':'str',
            'url':'str',
            'token':'str',
            'admin_username':'str',
            'password':'str',
            'otp_token':'str',
            'username':'str',
            'private_key':'int',
            'connect_timeout':'int',
            'sudo':'bool',
    })
    PrivateKey = typing.TypedDict('PrivateKey', {
            'generate_key':'bool',
            'existing_key_id':'int',
            'name':'str',
    })
    class SetupType(str,Enum):
        SEMIAUTOMATIC = 'SEMI-AUTOMATIC'
        MANUAL = 'MANUAL'
        ...
    SemiAutomaticSetup = typing.TypedDict('SemiAutomaticSetup', {
            'url':'str',
            'token':'str',
            'admin_username':'str',
            'password':'str',
            'otp_token':'str',
            'username':'str',
            'connect_timeout':'int',
            'sudo':'bool',
    })
    SetupSshConnection = typing.TypedDict('SetupSshConnection', {
            'private_key':'PrivateKey',
            'connection_name':'str',
            'setup_type':'SetupType',
            'semi_automatic_setup':'SemiAutomaticSetup',
            'manual_setup':'dict[str]',
    })
    KeychainCredentialUpdate = typing.TypedDict('KeychainCredentialUpdate', {
            'name':'str',
            'attributes':'dict[str]',
    })
    KeychaincredentialUpdateReturns = typing.TypedDict('KeychaincredentialUpdateReturns', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'id':'int',
    })
    CredentialResult = typing.TypedDict('CredentialResult', {
            'title':'str',
            'unbind_method':'str',
    })
