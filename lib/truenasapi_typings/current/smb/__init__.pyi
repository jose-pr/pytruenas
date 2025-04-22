from pytruenas import Namespace as _NS 
class Smb(_NS):
    
    def bindip_choices(self,
    ) -> SmbBindip_choices:
        """List of valid choices for IP addresses to which to bind the SMB service. Addresses assigned by DHCP are excluded from the results."""
        ...
    def config(self,
    ) -> SmbConfig:
        """"""
        ...
    def unixcharset_choices(self,
    ) -> SmbUnixcharset_choices:
        """"""
        ...
    def update(self,
        smb_update,
    ) -> SmbUpdate:
        """Update SMB Service Configuration.

`netbiosname` defaults to the original hostname of the system.

`netbiosalias` a list of netbios aliases. If Server is joined to an AD domain, additional Kerberos Service Principal Names will be generated for these aliases.

`workgroup` specifies the NetBIOS workgroup to which the TrueNAS server belongs. This will be automatically set to the correct value during the process of joining an AD domain. NOTE: `workgroup` and `netbiosname` should have different values.

`enable_smb1` allows legacy SMB clients to connect to the server when enabled.

`aapl_extensions` enables support for SMB2 protocol extensions for MacOS clients. This is not a requirement for MacOS support, but is currently a requirement for time machine support.

`localmaster` when set, determines if the system participates in a browser election.

`guest` attribute is specified to select the account to be used for guest access. It defaults to "nobody".

The group specified as the SMB `admin_group` will be automatically added as a foreign group member of S-1-5-32-544 (builtin\admins). This will afford the group all privileges granted to a local admin. Any SMB group may be selected (including AD groups).

`ntlmv1_auth` enables a legacy and insecure authentication method, which may be required for legacy or poorly-implemented SMB clients.

`encryption` set global server behavior with regard to SMB encrpytion. Options are DEFAULT (which follows the upstream defaults -- currently identical to NEGOTIATE), NEGOTIATE encrypts SMB transport only if requested by the SMB client, DESIRED encrypts SMB transport if supported by the SMB client, REQUIRED only allows encrypted transport to the SMB server. Mandatory SMB encryption is not compatible with SMB1 server support in TrueNAS.

`smb_options` smb.conf parameters that are not covered by the above supported configuration options may be added as an smb_option. Not all options are tested or supported, and behavior of smb_options may change between releases. Stability of smb.conf options is not guaranteed."""
        ...
class SmbBindip_choices:
    ...
class SmbConfig:
    ...
class SmbUnixcharset_choices:
    ...
class SmbUpdate:
    ... 