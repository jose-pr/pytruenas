
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Ldap(
    Namespace
    ):
    _namespace:typing.Literal['ldap']
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
            ldap_entry
        """
        ...
    @typing.overload
    def get_state(self, 
    /) -> 'DirectoryserviceState': 
        """
        Wrapper function for 'directoryservices.get_state'. Returns only the state of the
        LDAP service.

        Parameters
        ----------
        Returns
        -------
        DirectoryserviceState:
            directoryservice_state
        """
        ...
    @typing.overload
    def schema_choices(self, 
    /) -> 'list[NssInfoLdap]': 
        """
        Returns list of available LDAP schema choices.

        Parameters
        ----------
        Returns
        -------
        list[NssInfoLdap]:
            schema_choices
        """
        ...
    @typing.overload
    def ssl_choices(self, 
    /) -> 'list[Ssl]': 
        """
        Returns list of SSL choices.

        Parameters
        ----------
        Returns
        -------
        list[Ssl]:
            ssl_choices
        """
        ...
    @typing.overload
    def update(self, 
        ldap_update:'LdapUpdate',
    /) -> 'dict[str]': 
        """
        `hostname` list of ip addresses or hostnames of LDAP servers with
        which to communicate in order of preference. Failover only occurs
        if the current LDAP server is unresponsive.
        
        `basedn` specifies the default base DN to use when performing ldap
        operations. The base must be specified as a Distinguished Name in LDAP
        format.
        
        `binddn` specifies the default bind DN to use when performing ldap
        operations. The bind DN must be specified as a Distinguished Name in
        LDAP format.
        
        `anonbind` use anonymous authentication.
        
        `ssl` establish SSL/TLS-protected connections to the LDAP server(s).
        GSSAPI signing is disabled on SSL/TLS-protected connections if
        kerberos authentication is used.
        
        `certificate` LDAPs client certificate to be used for certificate-
        based authentication.
        
        `validate_certificates` specifies whether to perform checks on server
        certificates in a TLS session. If enabled, TLS_REQCERT demand is set.
        The server certificate is requested. If no certificate is provided or
        if a bad certificate is provided, the session is immediately terminated.
        If disabled, TLS_REQCERT allow is set. The server certificate is
        requested, but all errors are ignored.
        
        `kerberos_realm` in which the server is located. This parameter is
        only required for SASL GSSAPI authentication to the remote LDAP server.
        
        `kerberos_principal` kerberos principal to use for SASL GSSAPI
        authentication to the remote server. If `kerberos_realm` is specified
        without a keytab, then the `binddn` and `bindpw` are used to
        perform to obtain the ticket necessary for GSSAPI authentication.
        
        `timeout` specifies  a  timeout  (in  seconds) after which calls to
        synchronous LDAP APIs will abort if no response is received.
        
        `dns_timeout` specifies the timeout (in seconds) after which the
        poll(2)/select(2) following a connect(2) returns in case of no activity
        for openldap. For nslcd this specifies the time limit (in seconds) to
        use when connecting to the directory server. This directly impacts the
        length of time that the LDAP service tries before failing over to
        a secondary LDAP URI.
        
        `has_samba_schema` determines whether to configure samba to use the
        ldapsam passdb backend to provide SMB access to LDAP users. This feature
        requires the presence of Samba LDAP schema extensions on the remote
        LDAP server.

        Parameters
        ----------
        ldap_update:
            ldap_update
        Returns
        -------
        dict[str]:
            ldap_update_returns
        """
        ...
    class DirectoryserviceState(str,Enum):
        DISABLED = 'DISABLED'
        FAULTED = 'FAULTED'
        LEAVING = 'LEAVING'
        JOINING = 'JOINING'
        HEALTHY = 'HEALTHY'
        ...
    LdapUpdate = typing.TypedDict('LdapUpdate', {
            'hostname':'list',
            'basedn':'str',
            'binddn':'str',
            'bindpw':'str',
            'anonbind':'bool',
            'ssl':'Ssl',
            'certificate':'typing.Optional[int]',
            'validate_certificates':'bool',
            'disable_freenas_cache':'bool',
            'timeout':'int',
            'dns_timeout':'int',
            'kerberos_realm':'typing.Optional[int]',
            'kerberos_principal':'str',
            'has_samba_schema':'bool',
            'auxiliary_parameters':'str',
            'schema':'Schema',
            'enable':'bool',
    })
    class NssInfoLdap(str,Enum):
        RFC2307 = 'RFC2307'
        RFC2307BIS = 'RFC2307BIS'
        ...
    class Schema(str,Enum):
        RFC2307 = 'RFC2307'
        RFC2307BIS = 'RFC2307BIS'
        ...
    class Ssl(str,Enum):
        OFF = 'OFF'
        ON = 'ON'
        STARTTLS = 'START_TLS'
        ...
