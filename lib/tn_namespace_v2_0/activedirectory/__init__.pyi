
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Activedirectory(
    Namespace
    ):
    _namespace:typing.Literal['activedirectory']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def config(self, 
    /) -> 'dict[str]': 
        """
        

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            activedirectory_entry
        """
        ...
    @typing.overload
    def domain_info(self, 
        domain:'str',
    /) -> 'DomainInfo': 
        """
        Returns the following information about the currently joined domain:
        
        `LDAP server` IP address of current LDAP server to which TrueNAS is connected.
        
        `LDAP server name` DNS name of LDAP server to which TrueNAS is connected
        
        `Realm` Kerberos realm
        
        `LDAP port`
        
        `Server time` timestamp.
        
        `KDC server` Kerberos KDC to which TrueNAS is connected
        
        `Server time offset` current time offset from DC.
        
        `Last machine account password change`. timestamp

        Parameters
        ----------
        domain:
            domain
        Returns
        -------
        DomainInfo:
            domain_info
        """
        ...
    @typing.overload
    def get_state(self, 
    /) -> 'DirectoryserviceState': 
        """
        Wrapper function for 'directoryservices.get_state'. Returns only the state of the
        Active Directory service.

        Parameters
        ----------
        Returns
        -------
        DirectoryserviceState:
            directoryservice_state
        """
        ...
    @typing.overload
    def leave(self, 
        kerberos_username_password:'KerberosUsernamePassword',
    /) -> None: 
        """
        Leave Active Directory domain. This will remove computer
        object from AD and clear relevant configuration data from
        the NAS.
        This requires credentials for appropriately-privileged user.
        Credentials are used to obtain a kerberos ticket, which is
        used to perform the actual removal from the domain.

        Parameters
        ----------
        kerberos_username_password:
            kerberos_username_password
        Returns
        -------
        """
        ...
    @typing.overload
    def nss_info_choices(self, 
    /) -> 'NssInfoAd': 
        """
        Returns list of available LDAP schema choices.

        Parameters
        ----------
        Returns
        -------
        NssInfoAd:
            nss_info_ad
        """
        ...
    @typing.overload
    def started(self, 
    /) -> None: 
        """
        Issue a no-effect command to our DC. This checks if our secure channel connection to our
        domain controller is still alive. It has much less impact than wbinfo -t.
        Default winbind request timeout is 60 seconds, and can be adjusted by the smb4.conf parameter
        'winbind request timeout ='

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def update(self, 
        activedirectory_update:'ActivedirectoryUpdate',
    /) -> 'dict[str]': 
        """
        Update active directory configuration.
        `domainname` full DNS domain name of the Active Directory domain.
        
        `bindname` username used to perform the intial domain join.
        
        `bindpw` password used to perform the initial domain join. User-
        provided credentials are used to obtain a kerberos ticket, which
        is used to perform the actual domain join.
        
        `verbose_logging` increase logging during the domain join process.
        
        `use_default_domain` controls whether domain users and groups have
        the pre-windows 2000 domain name prepended to the user account. When
        enabled, the user appears as "administrator" rather than
        "EXAMPLEdministrator"
        
        `allow_trusted_doms` enable support for trusted domains. If this
        parameter is enabled, then separate idmap backends _must_ be configured
        for each trusted domain, and the idmap cache should be cleared.
        
        `allow_dns_updates` during the domain join process, automatically
        generate DNS entries in the AD domain for the NAS. If this is disabled,
        then a domain administrator must manually add appropriate DNS entries
        for the NAS. This parameter is recommended for TrueNAS HA servers.
        
        `disable_freenas_cache` disables active caching of AD users and groups.
        When disabled, only users cached in winbind's internal cache are
        visible in GUI dropdowns. Disabling active caching is recommended
        in environments with a large amount of users.
        
        `site` AD site of which the NAS is a member. This parameter is auto-
        detected during the domain join process. If no AD site is configured
        for the subnet in which the NAS is configured, then this parameter
        appears as 'Default-First-Site-Name'. Auto-detection is only performed
        during the initial domain join.
        
        `kerberos_realm` in which the server is located. This parameter is
        automatically populated during the initial domain join. If the NAS has
        an AD site configured and that site has multiple kerberos servers, then
        the kerberos realm is automatically updated with a site-specific
        configuration to use those servers. Auto-detection is only performed
        during initial domain join.
        
        `kerberos_principal` kerberos principal to use for AD-related
        operations outside of Samba. After intial domain join, this field is
        updated with the kerberos principal associated with the AD machine
        account for the NAS.
        
        `nss_info` controls how Winbind retrieves Name Service Information to
        construct a user's home directory and login shell. This parameter
        is only effective if the Active Directory Domain Controller supports
        the Microsoft Services for Unix (SFU) LDAP schema.
        
        `timeout` timeout value for winbind-related operations. This value may
        need to be increased in  environments with high latencies for
        communications with domain controllers or a large number of domain
        controllers. Lowering the value may cause status checks to fail.
        
        `dns_timeout` timeout value for DNS queries during the initial domain
        join. This value is also set as the NETWORK_TIMEOUT in the ldap config
        file.
        
        `createcomputer` Active Directory Organizational Unit in which new
        computer accounts are created.
        
        The OU string is read from top to bottom without RDNs. Slashes ("/")
        are used as delimiters, like `Computers/Servers/NAS`. The backslash
        ("\") is used to escape characters but not as a separator. Backslashes
        are interpreted at multiple levels and might require doubling or even
        quadrupling to take effect.
        
        When this field is blank, new computer accounts are created in the
        Active Directory default OU.
        
        The Active Directory service is started after a configuration
        update if the service was initially disabled, and the updated
        configuration sets `enable` to `True`. The Active Directory
        service is stopped if `enable` is changed to `False`. If the
        configuration is updated, but the initial `enable` state is `True`, and
        remains unchanged, then the samba server is only restarted.
        
        During the domain join, a kerberos keytab for the newly-created AD
        machine account is generated. It is used for all future
        LDAP / AD interaction and the user-provided credentials are removed.

        Parameters
        ----------
        activedirectory_update:
            activedirectory_update
        Returns
        -------
        dict[str]:
            activedirectory_update_returns
        """
        ...
    ActivedirectoryUpdate = typing.TypedDict('ActivedirectoryUpdate', {
            'domainname':'str',
            'bindname':'str',
            'bindpw':'str',
            'verbose_logging':'bool',
            'use_default_domain':'bool',
            'allow_trusted_doms':'bool',
            'allow_dns_updates':'bool',
            'disable_freenas_cache':'bool',
            'restrict_pam':'bool',
            'site':'typing.Optional[str]',
            'kerberos_realm':'typing.Optional[int]',
            'kerberos_principal':'typing.Optional[str]',
            'timeout':'int',
            'dns_timeout':'int',
            'nss_info':'typing.Optional[str]',
            'createcomputer':'str',
            'netbiosname':'str',
            'netbiosname_b':'str',
            'netbiosalias':'list',
            'enable':'bool',
    })
    class DirectoryserviceState(str,Enum):
        DISABLED = 'DISABLED'
        FAULTED = 'FAULTED'
        LEAVING = 'LEAVING'
        JOINING = 'JOINING'
        HEALTHY = 'HEALTHY'
        ...
    DomainInfo = typing.TypedDict('DomainInfo', {
            'LDAP server':'str',
            'LDAP server name':'str',
            'Realm':'str',
            'Bind Path':'str',
            'LDAP port':'int',
            'Server time':'int',
            'KDC server':'str',
            'Server time offset':'int',
            'Last machine account password change':'int',
    })
    KerberosUsernamePassword = typing.TypedDict('KerberosUsernamePassword', {
            'username':'str',
            'password':'str',
    })
    class NssInfoAd(str,Enum):
        SFU = 'SFU'
        SFU20 = 'SFU20'
        RFC2307 = 'RFC2307'
        ...
