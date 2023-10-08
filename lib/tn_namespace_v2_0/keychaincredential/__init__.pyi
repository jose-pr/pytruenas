
from pytruenas import Namespace, TrueNASClient
import typing
class Keychaincredential(Namespace):
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
        id:'str|int|bool|dict[str]|list',
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
    /) -> 'list[KeychainCredentialEntry]|KeychainCredentialEntry|int|KeychainCredentialEntry': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list[KeychainCredentialEntry]:
            
        KeychainCredentialEntry:
            
        int:
            
        KeychainCredentialEntry:
            
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
    /) -> 'KeychainCredentialEntry_': 
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
        KeychainCredentialEntry_:
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

class KeychainCredentialCreate(typing.TypedDict):
        name:'str'
        type:'str'
        attributes:'dict[str]'
        ...
class KeychaincredentialCreateReturns(typing.TypedDict):
        name:'str'
        type:'str'
        attributes:'dict[str]'
        id:'int'
        ...
class Options(typing.TypedDict):
        cascade:'bool'
        ...
class SshKeyPair(typing.TypedDict):
        private_key:'str'
        public_key:'str'
        ...
class QueryOptionsGetInstance(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class QueryOptions(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class KeychainCredentialEntry(typing.TypedDict):
        name:'str'
        type:'str'
        attributes:'dict[str]'
        id:'int'
        ...
class KeychainRemoteSshHostKeyScan(typing.TypedDict):
        host:'str'
        port:'str'
        connect_timeout:'int'
        ...
class KeychainRemoteSshSemiautomaticSetup(typing.TypedDict):
        name:'str'
        url:'str'
        token:'str'
        admin_username:'str'
        password:'str'
        otp_token:'str'
        username:'str'
        private_key:'int'
        connect_timeout:'int'
        sudo:'bool'
        ...
class KeychainCredentialEntry_(typing.TypedDict):
        name:'str'
        type:'str'
        attributes:'dict[str]'
        id:'int'
        ...
class SetupSshConnection(typing.TypedDict):
        private_key:'PrivateKey'
        connection_name:'str'
        setup_type:'str'
        semi_automatic_setup:'SemiAutomaticSetup'
        manual_setup:'dict[str]'
        ...
class PrivateKey(typing.TypedDict):
        generate_key:'bool'
        existing_key_id:'int'
        name:'str'
        ...
class SemiAutomaticSetup(typing.TypedDict):
        url:'str'
        token:'str'
        admin_username:'str'
        password:'str'
        otp_token:'str'
        username:'str'
        connect_timeout:'int'
        sudo:'bool'
        ...
class KeychainCredentialUpdate(typing.TypedDict):
        name:'str'
        attributes:'dict[str]'
        ...
class KeychaincredentialUpdateReturns(typing.TypedDict):
        name:'str'
        type:'str'
        attributes:'dict[str]'
        id:'int'
        ...
class CredentialResult(typing.TypedDict):
        title:'str'
        unbind_method:'str'
        ...
