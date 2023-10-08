
from pytruenas import Namespace, TrueNASClient
import typing
class Certificateauthority(Namespace):
    _namespace:typing.Literal['certificateauthority']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def ca_sign_csr(self, 
        ca_sign_csr:'CaSignCsr'={},
    /) -> 'CertificateEntry': 
        """
        Sign CSR by Certificate Authority of `ca_id`
        
        Sign CSR's and generate a certificate from it. `ca_id` provides which CA is to be used for signing
        a CSR of `csr_cert_id` which exists in the system
        
        `cert_extensions` can be specified if specific extensions are to be set in the newly signed certificate.

        Parameters
        ----------
        ca_sign_csr:
            ca_sign_csr
        Returns
        -------
        CertificateEntry:
            certificate_entry
        """
        ...
    @typing.overload
    def create(self, 
        ca_create:'CaCreate'={},
    /) -> 'CertificateauthorityCreateReturns': 
        """
        Create a new Certificate Authority
        
        Certificate Authorities are classified under following types with the necessary keywords to be passed
        for `create_type` attribute to create the respective type of certificate authority
        
        1) Internal Certificate Authority       -  CA_CREATE_INTERNAL
        
        2) Imported Certificate Authority       -  CA_CREATE_IMPORTED
        
        3) Intermediate Certificate Authority   -  CA_CREATE_INTERMEDIATE
        
        Created certificate authorities use RSA keys by default. If an Elliptic Curve Key is desired, then it can be
        specified with the `key_type` attribute. If the `ec_curve` attribute is not specified for the Elliptic
        Curve Key, default to using "SECP384R1" curve.
        
        A type is selected by the Certificate Authority Service based on `create_type`. The rest of the values
        are validated accordingly and finally a certificate is made based on the selected type.
        
        `cert_extensions` can be specified to set X509v3 extensions.

        Parameters
        ----------
        ca_create:
            ca_create
        Returns
        -------
        CertificateauthorityCreateReturns:
            certificateauthority_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete a Certificate Authority of `id`

        Parameters
        ----------
        id:
            Delete a Certificate Authority of `id`
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
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
    def profiles(self, 
    /) -> 'CertificateAuthorityProfiles': 
        """
        Returns a dictionary of predefined options for specific use cases i.e OpenVPN certificate authority
        configurations which can be used for creating certificate authorities.

        Parameters
        ----------
        Returns
        -------
        CertificateAuthorityProfiles:
            certificate_authority_profiles
        """
        ...
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'list[CertificateEntry_]|CertificateEntry_|int|CertificateEntry_': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list[CertificateEntry_]:
            
        CertificateEntry_:
            
        int:
            
        CertificateEntry_:
            
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        ca_update:'CaUpdate'={},
    /) -> 'CertificateauthorityUpdateReturns': 
        """
        Update Certificate Authority of `id`
        
        Only `name` and `revoked` attribute can be updated.
        
        If `revoked` is enabled, the CA and its complete chain is marked as revoked and added to the CA's
        certificate revocation list.

        Parameters
        ----------
        id:
            Update Certificate Authority of `id`
        ca_update:
            ca_update
        Returns
        -------
        CertificateauthorityUpdateReturns:
            certificateauthority_update_returns
        """
        ...

class CaSignCsr(typing.TypedDict):
        ca_id:'int'
        csr_cert_id:'int'
        name:'str'
        cert_extensions:'CertExtensions'
        ...
class CertExtensions(typing.TypedDict):
        BasicConstraints:'BasicConstraints'
        AuthorityKeyIdentifier:'AuthorityKeyIdentifier'
        ExtendedKeyUsage:'ExtendedKeyUsage'
        KeyUsage:'KeyUsage'
        ...
class BasicConstraints(typing.TypedDict):
        ca:'bool'
        enabled:'bool'
        path_length:'typing.Optional[int]'
        extension_critical:'bool'
        ...
class AuthorityKeyIdentifier(typing.TypedDict):
        authority_cert_issuer:'bool'
        enabled:'bool'
        extension_critical:'bool'
        ...
class ExtendedKeyUsage(typing.TypedDict):
        usages:'list[str]'
        enabled:'bool'
        extension_critical:'bool'
        ...
class KeyUsage(typing.TypedDict):
        enabled:'bool'
        digital_signature:'bool'
        content_commitment:'bool'
        key_encipherment:'bool'
        data_encipherment:'bool'
        key_agreement:'bool'
        key_cert_sign:'bool'
        crl_sign:'bool'
        encipher_only:'bool'
        decipher_only:'bool'
        extension_critical:'bool'
        ...
class CertificateEntry(typing.TypedDict):
        id:'int'
        type:'int'
        name:'str'
        certificate:'typing.Optional[str]'
        privatekey:'typing.Optional[str]'
        CSR:'typing.Optional[str]'
        acme_uri:'typing.Optional[str]'
        domains_authenticators:'dict[str]'
        renew_days:'int'
        revoked_date:'typing.Optional[str]'
        signedby:'dict[str]'
        root_path:'str'
        acme:'dict[str]'
        certificate_path:'typing.Optional[str]'
        privatekey_path:'typing.Optional[str]'
        csr_path:'typing.Optional[str]'
        cert_type:'str'
        revoked:'bool'
        expired:'typing.Optional[bool]'
        issuer:'typing.Union[str, NoneType, dict[str]]'
        chain_list:'list[str]'
        country:'typing.Optional[str]'
        state:'typing.Optional[str]'
        city:'typing.Optional[str]'
        organization:'typing.Optional[str]'
        organizational_unit:'typing.Optional[str]'
        san:'typing.Optional[list[str]]'
        email:'typing.Optional[str]'
        DN:'typing.Optional[str]'
        subject_name_hash:'typing.Optional[str]'
        digest_algorithm:'typing.Optional[str]'
        from:'typing.Optional[str]'
        common:'typing.Optional[str]'
        until:'typing.Optional[str]'
        fingerprint:'typing.Optional[str]'
        key_type:'typing.Optional[str]'
        internal:'typing.Optional[str]'
        lifetime:'typing.Optional[int]'
        serial:'typing.Optional[int]'
        key_length:'typing.Optional[int]'
        chain:'typing.Optional[bool]'
        CA_type_existing:'bool'
        CA_type_internal:'bool'
        CA_type_intermediate:'bool'
        cert_type_existing:'bool'
        cert_type_internal:'bool'
        cert_type_CSR:'bool'
        parsed:'bool'
        can_be_revoked:'bool'
        extensions:'dict[str]'
        revoked_certs:'list'
        crl_path:'str'
        signed_certificates:'int'
        ...
class CaCreate(typing.TypedDict):
        tos:'bool'
        csr_id:'int'
        signedby:'int'
        key_length:'int'
        renew_days:'int'
        type:'int'
        lifetime:'int'
        serial:'int'
        acme_directory_uri:'str'
        certificate:'str'
        city:'str'
        common:'typing.Optional[str]'
        country:'str'
        CSR:'str'
        ec_curve:'str'
        email:'str'
        key_type:'str'
        name:'str'
        organization:'str'
        organizational_unit:'str'
        passphrase:'str'
        privatekey:'str'
        state:'str'
        create_type:'str'
        digest_algorithm:'str'
        san:'list[str]'
        cert_extensions:'CertExtensions'
        add_to_trusted_store:'bool'
        ...
class CertExtensions_(typing.TypedDict):
        BasicConstraints:'BasicConstraints'
        AuthorityKeyIdentifier:'AuthorityKeyIdentifier'
        ExtendedKeyUsage:'ExtendedKeyUsage'
        KeyUsage:'KeyUsage'
        ...
class BasicConstraints_(typing.TypedDict):
        ca:'bool'
        enabled:'bool'
        path_length:'typing.Optional[int]'
        extension_critical:'bool'
        ...
class ExtendedKeyUsage_(typing.TypedDict):
        usages:'list[str]'
        enabled:'bool'
        extension_critical:'bool'
        ...
class KeyUsage_(typing.TypedDict):
        enabled:'bool'
        digital_signature:'bool'
        content_commitment:'bool'
        key_encipherment:'bool'
        data_encipherment:'bool'
        key_agreement:'bool'
        key_cert_sign:'bool'
        crl_sign:'bool'
        encipher_only:'bool'
        decipher_only:'bool'
        extension_critical:'bool'
        ...
class CertificateauthorityCreateReturns(typing.TypedDict):
        id:'int'
        type:'int'
        name:'str'
        certificate:'typing.Optional[str]'
        privatekey:'typing.Optional[str]'
        CSR:'typing.Optional[str]'
        acme_uri:'typing.Optional[str]'
        domains_authenticators:'dict[str]'
        renew_days:'int'
        revoked_date:'typing.Optional[str]'
        signedby:'dict[str]'
        root_path:'str'
        acme:'dict[str]'
        certificate_path:'typing.Optional[str]'
        privatekey_path:'typing.Optional[str]'
        csr_path:'typing.Optional[str]'
        cert_type:'str'
        revoked:'bool'
        expired:'typing.Optional[bool]'
        issuer:'typing.Union[str, NoneType, dict[str]]'
        chain_list:'list[str]'
        country:'typing.Optional[str]'
        state:'typing.Optional[str]'
        city:'typing.Optional[str]'
        organization:'typing.Optional[str]'
        organizational_unit:'typing.Optional[str]'
        san:'typing.Optional[list[str]]'
        email:'typing.Optional[str]'
        DN:'typing.Optional[str]'
        subject_name_hash:'typing.Optional[str]'
        digest_algorithm:'typing.Optional[str]'
        from:'typing.Optional[str]'
        common:'typing.Optional[str]'
        until:'typing.Optional[str]'
        fingerprint:'typing.Optional[str]'
        key_type:'typing.Optional[str]'
        internal:'typing.Optional[str]'
        lifetime:'typing.Optional[int]'
        serial:'typing.Optional[int]'
        key_length:'typing.Optional[int]'
        chain:'typing.Optional[bool]'
        CA_type_existing:'bool'
        CA_type_internal:'bool'
        CA_type_intermediate:'bool'
        cert_type_existing:'bool'
        cert_type_internal:'bool'
        cert_type_CSR:'bool'
        parsed:'bool'
        can_be_revoked:'bool'
        extensions:'dict[str]'
        revoked_certs:'list'
        crl_path:'str'
        signed_certificates:'int'
        add_to_trusted_store:'bool'
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
class CertificateAuthorityProfiles(typing.TypedDict):
        CA:'dict[str]'
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
class CertificateEntry_(typing.TypedDict):
        id:'int'
        type:'int'
        name:'str'
        certificate:'typing.Optional[str]'
        privatekey:'typing.Optional[str]'
        CSR:'typing.Optional[str]'
        acme_uri:'typing.Optional[str]'
        domains_authenticators:'dict[str]'
        renew_days:'int'
        revoked_date:'typing.Optional[str]'
        signedby:'dict[str]'
        root_path:'str'
        acme:'dict[str]'
        certificate_path:'typing.Optional[str]'
        privatekey_path:'typing.Optional[str]'
        csr_path:'typing.Optional[str]'
        cert_type:'str'
        revoked:'bool'
        expired:'typing.Optional[bool]'
        issuer:'typing.Union[str, NoneType, dict[str]]'
        chain_list:'list[str]'
        country:'typing.Optional[str]'
        state:'typing.Optional[str]'
        city:'typing.Optional[str]'
        organization:'typing.Optional[str]'
        organizational_unit:'typing.Optional[str]'
        san:'typing.Optional[list[str]]'
        email:'typing.Optional[str]'
        DN:'typing.Optional[str]'
        subject_name_hash:'typing.Optional[str]'
        digest_algorithm:'typing.Optional[str]'
        from:'typing.Optional[str]'
        common:'typing.Optional[str]'
        until:'typing.Optional[str]'
        fingerprint:'typing.Optional[str]'
        key_type:'typing.Optional[str]'
        internal:'typing.Optional[str]'
        lifetime:'typing.Optional[int]'
        serial:'typing.Optional[int]'
        key_length:'typing.Optional[int]'
        chain:'typing.Optional[bool]'
        CA_type_existing:'bool'
        CA_type_internal:'bool'
        CA_type_intermediate:'bool'
        cert_type_existing:'bool'
        cert_type_internal:'bool'
        cert_type_CSR:'bool'
        parsed:'bool'
        can_be_revoked:'bool'
        extensions:'dict[str]'
        revoked_certs:'list'
        crl_path:'str'
        signed_certificates:'int'
        add_to_trusted_store:'bool'
        ...
class CaUpdate(typing.TypedDict):
        revoked:'bool'
        add_to_trusted_store:'bool'
        ca_id:'int'
        csr_cert_id:'int'
        create_type:'str'
        name:'str'
        ...
class CertificateauthorityUpdateReturns(typing.TypedDict):
        id:'int'
        type:'int'
        name:'str'
        certificate:'typing.Optional[str]'
        privatekey:'typing.Optional[str]'
        CSR:'typing.Optional[str]'
        acme_uri:'typing.Optional[str]'
        domains_authenticators:'dict[str]'
        renew_days:'int'
        revoked_date:'typing.Optional[str]'
        signedby:'dict[str]'
        root_path:'str'
        acme:'dict[str]'
        certificate_path:'typing.Optional[str]'
        privatekey_path:'typing.Optional[str]'
        csr_path:'typing.Optional[str]'
        cert_type:'str'
        revoked:'bool'
        expired:'typing.Optional[bool]'
        issuer:'typing.Union[str, NoneType, dict[str]]'
        chain_list:'list[str]'
        country:'typing.Optional[str]'
        state:'typing.Optional[str]'
        city:'typing.Optional[str]'
        organization:'typing.Optional[str]'
        organizational_unit:'typing.Optional[str]'
        san:'typing.Optional[list[str]]'
        email:'typing.Optional[str]'
        DN:'typing.Optional[str]'
        subject_name_hash:'typing.Optional[str]'
        digest_algorithm:'typing.Optional[str]'
        from:'typing.Optional[str]'
        common:'typing.Optional[str]'
        until:'typing.Optional[str]'
        fingerprint:'typing.Optional[str]'
        key_type:'typing.Optional[str]'
        internal:'typing.Optional[str]'
        lifetime:'typing.Optional[int]'
        serial:'typing.Optional[int]'
        key_length:'typing.Optional[int]'
        chain:'typing.Optional[bool]'
        CA_type_existing:'bool'
        CA_type_internal:'bool'
        CA_type_intermediate:'bool'
        cert_type_existing:'bool'
        cert_type_internal:'bool'
        cert_type_CSR:'bool'
        parsed:'bool'
        can_be_revoked:'bool'
        extensions:'dict[str]'
        revoked_certs:'list'
        crl_path:'str'
        signed_certificates:'int'
        add_to_trusted_store:'bool'
        ...
