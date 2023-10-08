
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Smb(Namespace):
    _namespace:_ty.Literal['smb']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def bindip_choices(self, 
    /) -> None: 
        """
        List of valid choices for IP addresses to which to bind the SMB service.
        Addresses assigned by DHCP are excluded from the results.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @_ty.overload
    def client_count(self, 
    /) -> None: 
        """
        Return currently connected clients count.

        Parameters
        ----------
        Returns
        -------
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
            smb_entry
        """
        ...
    @_ty.overload
    def domain_choices(self, 
    /) -> None: 
        """
        List of domains visible to winbindd. Returns empty list if winbindd is
        stopped.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @_ty.overload
    def get_remote_acl(self, 
        get_remote_acl:'dict[str]'={},
    /) -> None: 
        """
        Retrieves an ACL from a remote SMB server.
        
        `server` IP Address or hostname of the remote server
        
        `share` Share name
        
        `path` path on the remote SMB server. Use "" to separate path components
        
        `username` username to use for authentication
        
        `password` password to use for authentication
        
        `use_kerberos` use credentials to get a kerberos ticket for authentication.
        AD only.
        
        `output_format` format for resulting ACL data. Choices are either 'SMB',
        which will present the information as a Windows SD or 'LOCAL', which formats
        the ACL information according local filesystem of the TrueNAS server.

        Parameters
        ----------
        get_remote_acl:
            get_remote_acl
        Returns
        -------
        """
        ...
    @_ty.overload
    def status(self, 
        info_level:'str'="ALL",
        query_filters:'list'=[],
        query_options:'dict[str]'={},
        status_options:'dict[str]'={},
    /) -> None: 
        """
        Returns SMB server status (sessions, open files, locks, notifications).
        
        `info_level` type of information requests. Defaults to ALL.
        
        `status_options` additional options to filter query results. Supported
        values are as follows: `verbose` gives more verbose status output
        `fast` causes smbstatus to not check if the status data is valid by
        checking if the processes that the status data refer to all still
        exist. This speeds up execution on busy systems and clusters but
        might display stale data of processes that died without cleaning up
        properly. `restrict_user` specifies the limits results to the specified
        user.

        Parameters
        ----------
        info_level:
            `info_level` type of information requests. Defaults to ALL.
        query_filters:
            query-filters
        query_options:
            query-options
        status_options:
            `status_options` additional options to filter query results. Supported
            values are as follows: `verbose` gives more verbose status output
        Returns
        -------
        """
        ...
    @_ty.overload
    def unixcharset_choices(self, 
    /) -> None: 
        """
        

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @_ty.overload
    def update(self, 
        smb_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update SMB Service Configuration.
        
        `netbiosname` defaults to the original hostname of the system.
        
        `netbiosalias` a list of netbios aliases. If Server is joined to an AD domain, additional Kerberos
        Service Principal Names will be generated for these aliases.
        
        `workgroup` specifies the NetBIOS workgroup to which the TrueNAS server belongs. This will be
        automatically set to the correct value during the process of joining an AD domain.
        NOTE: `workgroup` and `netbiosname` should have different values.
        
        `enable_smb1` allows legacy SMB clients to connect to the server when enabled.
        
        `aapl_extensions` enables support for SMB2 protocol extensions for MacOS clients. This is not a
        requirement for MacOS support, but is currently a requirement for time machine support.
        
        `localmaster` when set, determines if the system participates in a browser election.
        
        `guest` attribute is specified to select the account to be used for guest access. It defaults to "nobody".
        
        The group specified as the SMB `admin_group` will be automatically added as a foreign group member
        of S-1-5-32-544 (builtindmins). This will afford the group all privileges granted to a local admin.
        Any SMB group may be selected (including AD groups).
        
        `ntlmv1_auth` enables a legacy and insecure authentication method, which may be required for legacy or
        poorly-implemented SMB clients.
        
        `smb_options` smb.conf parameters that are not covered by the above supported configuration options may be
        added as an smb_option. Not all options are tested or supported, and behavior of smb_options may change
        between releases. Stability of smb.conf options is not guaranteed.

        Parameters
        ----------
        smb_update:
            smb_update
        Returns
        -------
        dict[str]:
            smb_update_returns
        """
        ...
