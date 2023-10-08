
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Nfs(Namespace):
    _namespace:_ty.Literal['nfs']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def add_principal(self, 
        kerberos_username_password:'dict[str]'={},
    /) -> 'bool': 
        """
        Use user-provided admin credentials to kinit, add NFS SPN
        entries to the remote kerberos server, and then append the new entries
        to our system keytab.
        
        Currently this is only supported in AD environments.

        Parameters
        ----------
        kerberos_username_password:
            kerberos_username_password
        Returns
        -------
        bool:
            principal_add_status
        """
        ...
    @_ty.overload
    def bindip_choices(self, 
    /) -> 'dict[str]': 
        """
        Returns ip choices for NFS service to use

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            bindip_choices
        """
        ...
    @_ty.overload
    def client_count(self, 
    /) -> 'int': 
        """
        Return currently connected clients count.
        Count may not be accurate if NFSv3 protocol is in use
        due to potentially stale rmtab entries.

        Parameters
        ----------
        Returns
        -------
        int:
            number_of_clients
        """
        ...
    @_ty.overload
    def config(self, 
    /) -> 'dict[str]': 
        """
        

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            nfs_entry
        """
        ...
    @_ty.overload
    def get_nfs3_clients(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> None: 
        """
        Read contents of rmtab. This information may not
        be accurate due to stale entries. This is ultimately
        a limitation of the NFSv3 protocol.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        """
        ...
    @_ty.overload
    def get_nfs4_clients(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> None: 
        """
        Read information about NFSv4 clients from
        /proc/fs/nfsd/clients

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        """
        ...
    @_ty.overload
    def update(self, 
        nfs_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update NFS Service Configuration.
        
        `servers` represents number of servers to create.
        
        When `allow_nonroot` is set, it allows non-root mount requests to be served.
        
        `bindip` is a list of IP's on which NFS will listen for requests. When it is unset/empty, NFS listens on
        all available addresses.
        
        `protocols` specifies whether NFSv3, NFSv4, or both are enabled.
        
        `v4_v3owner` when set means that system will use NFSv3 ownership model for NFSv4.
        
        `v4_krb` will force NFS shares to fail if the Kerberos ticket is unavailable.
        
        `v4_domain` overrides the default DNS domain name for NFSv4.
        
        `mountd_port` specifies the port mountd(8) binds to.
        
        `rpcstatd_port` specifies the port rpc.statd(8) binds to.
        
        `rpclockd_port` specifies the port rpclockd_port(8) binds to.

        Parameters
        ----------
        nfs_update:
            nfs_update
        Returns
        -------
        dict[str]:
            nfs_update_returns
        """
        ...
