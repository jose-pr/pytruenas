
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Keychaincredential(Namespace):
    _namespace:_ty.Literal['keychaincredential']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        keychain_credential_create:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            keychaincredential_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
        options:'dict[str]'={},
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
    @_ty.overload
    def generate_ssh_key_pair(self, 
    /) -> 'dict[str]': 
        """
        Generate a public/private key pair
        
        Generate a public/private key pair (useful for `SSH_KEY_PAIR` type)

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            ssh_key_pair
        """
        ...
    @_ty.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'dict[str]'={},
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
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @_ty.overload
    def remote_ssh_host_key_scan(self, 
        keychain_remote_ssh_host_key_scan:'dict[str]'={},
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
    @_ty.overload
    def remote_ssh_semiautomatic_setup(self, 
        keychain_remote_ssh_semiautomatic_setup:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            keychain_credential_entry
        """
        ...
    @_ty.overload
    def setup_ssh_connection(self, 
        setup_ssh_connection:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            keychain_credential_entry
        """
        ...
    @_ty.overload
    def update(self, 
        id:'int',
        keychain_credential_update:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            keychaincredential_update_returns
        """
        ...
    @_ty.overload
    def used_by(self, 
        id:'int',
    /) -> 'list': 
        """
        Returns list of objects that use this credential.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        list:
            credential_results
        """
        ...
