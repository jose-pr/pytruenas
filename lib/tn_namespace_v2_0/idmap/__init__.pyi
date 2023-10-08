
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Idmap(Namespace):
    _namespace:_ty.Literal['idmap']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def backend_choices(self, 
    /) -> None: 
        """
        Returns array of valid idmap backend choices per directory service.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @_ty.overload
    def backend_options(self, 
    /) -> None: 
        """
        This returns full information about idmap backend options. Not all
        `options` are valid for every backend.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @_ty.overload
    def clear_idmap_cache(self, 
    /) -> None: 
        """
        Stop samba, remove the winbindd_cache.tdb file, start samba, flush samba's cache.
        This should be performed after finalizing idmap changes.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @_ty.overload
    def create(self, 
        idmap_domain_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create a new IDMAP domain. These domains must be unique. This table
        will be automatically populated after joining an Active Directory domain
        if "allow trusted domains" is set to True in the AD service configuration.
        There are three default system domains: DS_TYPE_ACTIVEDIRECTORY, DS_TYPE_LDAP, DS_TYPE_DEFAULT_DOMAIN.
        The system domains correspond with the idmap settings under Active Directory, LDAP, and SMB
        respectively.
        
        `name` the pre-windows 2000 domain name.
        
        `DNS_domain_name` DNS name of the domain.
        
        `idmap_backend` provides a plugin interface for Winbind to use varying
        backends to store SID/uid/gid mapping tables. The correct setting
        depends on the environment in which the NAS is deployed.
        
        `range_low` and `range_high` specify the UID and GID range for which this backend is authoritative.
        
        `certificate_id` references the certificate ID of the SSL certificate to use for certificate-based
        authentication to a remote LDAP server. This parameter is not supported for all idmap backends as some
        backends will generate SID to ID mappings algorithmically without causing network traffic.
        
        `options` are additional parameters that are backend-dependent:
        
        `AD` idmap backend options:
        `unix_primary_group` If True, the primary group membership is fetched from the LDAP attributes (gidNumber).
        If False, the primary group membership is calculated via the "primaryGroupID" LDAP attribute.
        
        `unix_nss_info` if True winbind will retrieve the login shell and home directory from the LDAP attributes.
        If False or if the AD LDAP entry lacks the SFU attributes the smb4.conf parameters `template shell` and `template homedir` are used.
        
        `schema_mode` Defines the schema that idmap_ad should use when querying Active Directory regarding user and group information.
        This can be either the RFC2307 schema support included in Windows 2003 R2 or the Service for Unix (SFU) schema.
        For SFU 3.0 or 3.5 please choose "SFU", for SFU 2.0 please choose "SFU20". The behavior of primary group membership is
        controlled by the unix_primary_group option.
        
        `AUTORID` idmap backend options:
        `readonly` sets the module to read-only mode. No new ranges will be allocated and new mappings
        will not be created in the idmap pool.
        
        `ignore_builtin` ignores mapping requests for the BUILTIN domain.
        
        `LDAP` idmap backend options:
        `ldap_base_dn` defines the directory base suffix to use for SID/uid/gid mapping entries.
        
        `ldap_user_dn` defines the user DN to be used for authentication.
        
        `ldap_url` specifies the LDAP server to use for SID/uid/gid map entries.
        
        `ssl` specifies whether to encrypt the LDAP transport for the idmap backend.
        
        `NSS` idmap backend options:
        `linked_service` specifies the auxiliary directory service ID provider.
        
        `RFC2307` idmap backend options:
        `domain` specifies the domain for which the idmap backend is being created. Numeric id, short-form
        domain name, or long-form DNS domain name of the domain may be specified. Entry must be entered as
        it appears in `idmap.domain`.
        
        `range_low` and `range_high` specify the UID and GID range for which this backend is authoritative.
        
        `ldap_server` defines the type of LDAP server to use. This can either be an LDAP server provided
        by the Active Directory Domain (ad) or a stand-alone LDAP server.
        
        `bind_path_user` specfies the search base where user objects can be found in the LDAP server.
        
        `bind_path_group` specifies the search base where group objects can be found in the LDAP server.
        
        `user_cn` query cn attribute instead of uid attribute for the user name in LDAP.
        
        `realm` append @realm to cn for groups (and users if user_cn is set) in LDAP queries.
        
        `ldmap_domain` when using the LDAP server in the Active Directory server, this allows one to
        specify the domain where to access the Active Directory server. This allows using trust relationships
        while keeping all RFC 2307 records in one place. This parameter is optional, the default is to access
        the AD server in the current domain to query LDAP records.
        
        `ldap_url` when using a stand-alone LDAP server, this parameter specifies the LDAP URL for accessing the LDAP server.
        
        `ldap_user_dn` defines the user DN to be used for authentication.
        
        `ldap_user_dn_password` is the password to be used for LDAP authentication.
        
        `realm` defines the realm to use in the user and group names. This is only required when using cn_realm together with
         a stand-alone ldap server.
        
        `RID` backend options:
        `sssd_compat` generate idmap low range based on same algorithm that SSSD uses by default.

        Parameters
        ----------
        idmap_domain_create:
            idmap_domain_create
        Returns
        -------
        dict[str]:
            idmap_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete a domain by id. Deletion of default system domains is not permitted.
        In case of registry config for clustered server, this will remove all smb4.conf
        entries for the domain associated with the id.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
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
    def options_choices(self, 
        idmap_backend:'str',
    /) -> None: 
        """
        Returns a list of supported keys for the specified idmap backend.

        Parameters
        ----------
        idmap_backend:
            idmap_backend
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
    def update(self, 
        id:'int',
        idmap_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update a domain by id.

        Parameters
        ----------
        id:
            id
        idmap_update:
            idmap_update
        Returns
        -------
        dict[str]:
            idmap_update_returns
        """
        ...
