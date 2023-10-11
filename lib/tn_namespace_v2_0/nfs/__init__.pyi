
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Nfs(
    Namespace
    ):
    _namespace:typing.Literal['nfs']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def add_principal(self, 
        kerberos_username_password:'KerberosUsernamePassword',
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
    @typing.overload
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
    @typing.overload
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
    @typing.overload
    def config(self, 
    /) -> 'NfsEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        NfsEntry:
            nfs_entry
        """
        ...
    @typing.overload
    def get_nfs3_clients(self, 
        query_filters:'list[list]',
        query_options:'QueryOptions',
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
    @typing.overload
    def get_nfs4_clients(self, 
        query_filters:'list[list]',
        query_options:'QueryOptions',
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
    @typing.overload
    def update(self, 
        nfs_update:'NfsUpdate',
    /) -> 'NfsUpdateReturns': 
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
        NfsUpdateReturns:
            nfs_update_returns
        """
        ...
    KerberosUsernamePassword = typing.TypedDict('KerberosUsernamePassword', {
            'username':'str',
            'password':'str',
    })
    NfsEntry = typing.TypedDict('NfsEntry', {
            'id':'int',
            'servers':'int',
            'udp':'bool',
            'allow_nonroot':'bool',
            'protocols':'list[Protocol]',
            'v4_v3owner':'bool',
            'v4_krb':'bool',
            'v4_domain':'str',
            'bindip':'list[str]',
            'mountd_port':'typing.Optional[int]',
            'rpcstatd_port':'typing.Optional[int]',
            'rpclockd_port':'typing.Optional[int]',
            'mountd_log':'bool',
            'statd_lockd_log':'bool',
            'v4_krb_enabled':'bool',
            'userd_manage_gids':'bool',
    })
    class Protocol(str,Enum):
        NFSV3 = 'NFSV3'
        NFSV4 = 'NFSV4'
        ...
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
    NfsUpdate = typing.TypedDict('NfsUpdate', {
            'servers':'int',
            'udp':'bool',
            'allow_nonroot':'bool',
            'protocols':'list[Protocol]',
            'v4_v3owner':'bool',
            'v4_krb':'bool',
            'v4_domain':'str',
            'bindip':'list[str]',
            'mountd_port':'typing.Optional[int]',
            'rpcstatd_port':'typing.Optional[int]',
            'rpclockd_port':'typing.Optional[int]',
            'mountd_log':'bool',
            'statd_lockd_log':'bool',
            'userd_manage_gids':'bool',
    })
    NfsUpdateReturns = typing.TypedDict('NfsUpdateReturns', {
            'id':'int',
            'servers':'int',
            'udp':'bool',
            'allow_nonroot':'bool',
            'protocols':'list[Protocol]',
            'v4_v3owner':'bool',
            'v4_krb':'bool',
            'v4_domain':'str',
            'bindip':'list[str]',
            'mountd_port':'typing.Optional[int]',
            'rpcstatd_port':'typing.Optional[int]',
            'rpclockd_port':'typing.Optional[int]',
            'mountd_log':'bool',
            'statd_lockd_log':'bool',
            'v4_krb_enabled':'bool',
            'userd_manage_gids':'bool',
    })
