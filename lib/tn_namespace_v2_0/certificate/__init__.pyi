
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Certificate(
    Namespace
    ):
    _namespace:typing.Literal['certificate']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def acme_server_choices(self, 
    /) -> 'dict[str]': 
        """
        Dictionary of popular ACME Servers with their directory URI endpoints which we display automatically
        in UI

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            acme_server_choices
        """
        ...
    @typing.overload
    def certificate_signing_requests_profiles(self, 
    /) -> 'CertificateSigningRequestsProfiles': 
        """
        Returns a dictionary of predefined options for specific use cases i.e openvpn client/server
        configurations which can be used for creating certificate signing requests.

        Parameters
        ----------
        Returns
        -------
        CertificateSigningRequestsProfiles:
            Example(s):
            ```
            {
                "HTTPS RSA Certificate": {
                    "cert_extensions": {
                        "BasicConstraints": {
                            "enabled": true,
                            "ca": false,
                            "extension_critical": true
                        },
                        "ExtendedKeyUsage": {
                            "enabled": true,
                            "extension_critical": true,
                            "usages": [
                                "SERVER_AUTH",
                                "CLIENT_AUTH"
                            ]
                        },
                        "KeyUsage": {
                            "enabled": true,
                            "extension_critical": true,
                            "digital_signature": true,
                            "key_encipherment": true,
                            "key_agreement": true
                        }
                    },
                    "key_length": 2048,
                    "key_type": "RSA",
                    "lifetime": 397,
                    "digest_algorithm": "SHA256"
                },
                "HTTPS ECC Certificate": {
                    "cert_extensions": {
                        "BasicConstraints": {
                            "enabled": true,
                            "ca": false,
                            "extension_critical": true
                        },
                        "ExtendedKeyUsage": {
                            "enabled": true,
                            "extension_critical": true,
                            "usages": [
                                "SERVER_AUTH",
                                "CLIENT_AUTH"
                            ]
                        },
                        "KeyUsage": {
                            "enabled": true,
                            "extension_critical": true,
                            "digital_signature": true
                        }
                    },
                    "ec_curve": "SECP384R1",
                    "key_type": "EC",
                    "lifetime": 397,
                    "digest_algorithm": "SHA256"
                }
            }
            ```
        """
        ...
    @typing.overload
    def country_choices(self, 
    /) -> 'dict[str]': 
        """
        Returns country choices for creating a certificate/csr.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            country_choices
        """
        ...
    @typing.overload
    def create(self, 
        _certificate_create:'CertificateCreate',
    /) -> 'CertificateCreateReturns': 
        """
        Create a new Certificate
        
        Certificates are classified under following types and the necessary keywords to be passed
        for `create_type` attribute to create the respective type of certificate
        
        1) Internal Certificate                 -  CERTIFICATE_CREATE_INTERNAL
        
        2) Imported Certificate                 -  CERTIFICATE_CREATE_IMPORTED
        
        3) Certificate Signing Request          -  CERTIFICATE_CREATE_CSR
        
        4) Imported Certificate Signing Request -  CERTIFICATE_CREATE_IMPORTED_CSR
        
        5) ACME Certificate                     -  CERTIFICATE_CREATE_ACME
        
        By default, created certs use RSA keys. If an Elliptic Curve Key is desired, it can be specified with the
        `key_type` attribute. If the `ec_curve` attribute is not specified for the Elliptic Curve Key, then default to
        using "SECP384R1" curve.
        
        A type is selected by the Certificate Service based on `create_type`. The rest of the values in `data` are
        validated accordingly and finally a certificate is made based on the selected type.
        
        `cert_extensions` can be specified to set X509v3 extensions.

        Parameters
        ----------
        certificate_create:
            certificate_create
        Returns
        -------
        CertificateCreateReturns:
            certificate_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        _id:'int',
        _force:'bool',
    /) -> 'bool': 
        """
        Delete certificate of `id`.
        
        If the certificate is an ACME based certificate, certificate service will try to
        revoke the certificate by updating it's status with the ACME server, if it fails an exception is raised
        and the certificate is not deleted from the system. However, if `force` is set to True, certificate is deleted
        from the system even if some error occurred while revoking the certificate with the ACME Server

        Parameters
        ----------
        id:
            Delete certificate of `id`.
        force:
            If the certificate is an ACME based certificate, certificate service will try to
            revoke the certificate by updating it's status with the ACME server, if it fails an exception is raised
            and the certificate is not deleted from the system. However, if `force` is set to True, certificate is deleted
            from the system even if some error occurred while revoking the certificate with the ACME Server
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
        """
        ...
    @typing.overload
    def ec_curve_choices(self, 
    /) -> 'EcCurveChoices': 
        """
        Dictionary of supported EC curves.

        Parameters
        ----------
        Returns
        -------
        EcCurveChoices:
            ec_curve_choices
        """
        ...
    @typing.overload
    def extended_key_usage_choices(self, 
    /) -> 'ExtendedKeyUsageChoices': 
        """
        Dictionary of choices for `ExtendedKeyUsage` extension which can be passed over to `usages` attribute.

        Parameters
        ----------
        Returns
        -------
        ExtendedKeyUsageChoices:
            extended_key_usage_choices
        """
        ...
    @typing.overload
    def get_instance(self, 
        _id:'typing.Union[str, int, bool, dict[str], list]',
        _query_options_get_instance:'QueryOptionsGetInstance',
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
    def key_type_choices(self, 
    /) -> 'PrivateKeyTypeChoices': 
        """
        Dictionary of supported key types for certificates.

        Parameters
        ----------
        Returns
        -------
        PrivateKeyTypeChoices:
            private_key_type_choices
        """
        ...
    @typing.overload
    def profiles(self, 
    /) -> 'CertificateProfiles': 
        """
        Returns a dictionary of predefined options for specific use cases i.e openvpn client/server
        configurations which can be used for creating certificates.

        Parameters
        ----------
        Returns
        -------
        CertificateProfiles:
            certificate_profiles
        """
        ...
    @typing.overload
    def query(self, 
        _query_filters:'list[list]',
        _query_options:'QueryOptions',
    /) -> 'typing.Union[list[CertificateEntry], CertificateEntry, int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[CertificateEntry], CertificateEntry, int]:
            
        """
        ...
    @typing.overload
    def update(self, 
        _id:'int',
        _certificate_update:'CertificateUpdate',
    /) -> 'CertificateUpdateReturns': 
        """
        Update certificate of `id`
        
        Only name and revoked attribute can be updated.
        
        When `revoked` is enabled, the specified cert `id` is revoked and if it belongs to a CA chain which
        exists on this system, its serial number is added to the CA's certificate revocation list.

        Parameters
        ----------
        id:
            Update certificate of `id`
            When `revoked` is enabled, the specified cert `id` is revoked and if it belongs to a CA chain which
            exists on this system, its serial number is added to the CA's certificate revocation list.
        certificate_update:
            certificate_update
        Returns
        -------
        CertificateUpdateReturns:
            certificate_update_returns
        """
        ...
    AuthorityKeyIdentifier = typing.TypedDict('AuthorityKeyIdentifier', {
            'authority_cert_issuer':'bool',
            'enabled':'bool',
            'extension_critical':'bool',
    })
    BasicConstraints = typing.TypedDict('BasicConstraints', {
            'ca':'bool',
            'enabled':'bool',
            'path_length':'typing.Optional[int]',
            'extension_critical':'bool',
    })
    CertExtensions = typing.TypedDict('CertExtensions', {
            'BasicConstraints':'BasicConstraints',
            'AuthorityKeyIdentifier':'AuthorityKeyIdentifier',
            'ExtendedKeyUsage':'ExtendedKeyUsage',
            'KeyUsage':'KeyUsage',
    })
    CertificateCreate = typing.TypedDict('CertificateCreate', {
            'tos':'bool',
            'dns_mapping':'dict[str]',
            'csr_id':'int',
            'signedby':'int',
            'key_length':'int',
            'renew_days':'int',
            'type':'int',
            'lifetime':'int',
            'serial':'int',
            'acme_directory_uri':'str',
            'certificate':'str',
            'city':'str',
            'common':'typing.Optional[str]',
            'country':'str',
            'CSR':'str',
            'ec_curve':'EcCurve',
            'email':'str',
            'key_type':'KeyType',
            'name':'str',
            'organization':'str',
            'organizational_unit':'str',
            'passphrase':'str',
            'privatekey':'str',
            'state':'str',
            'create_type':'CreateType',
            'digest_algorithm':'DigestAlgorithm',
            'san':'list[str]',
            'cert_extensions':'CertExtensions',
    })
    CertificateCreateReturns = typing.TypedDict('CertificateCreateReturns', {
            'id':'int',
            'type':'int',
            'name':'str',
            'certificate':'typing.Optional[str]',
            'privatekey':'typing.Optional[str]',
            'CSR':'typing.Optional[str]',
            'acme_uri':'typing.Optional[str]',
            'domains_authenticators':'dict[str]',
            'renew_days':'int',
            'revoked_date':'typing.Optional[str]',
            'signedby':'dict[str]',
            'root_path':'str',
            'acme':'dict[str]',
            'certificate_path':'typing.Optional[str]',
            'privatekey_path':'typing.Optional[str]',
            'csr_path':'typing.Optional[str]',
            'cert_type':'str',
            'revoked':'bool',
            'expired':'typing.Optional[bool]',
            'issuer':'typing.Union[str, NoneType, dict[str]]',
            'chain_list':'list[str]',
            'country':'typing.Optional[str]',
            'state':'typing.Optional[str]',
            'city':'typing.Optional[str]',
            'organization':'typing.Optional[str]',
            'organizational_unit':'typing.Optional[str]',
            'san':'typing.Optional[list]',
            'email':'typing.Optional[str]',
            'DN':'typing.Optional[str]',
            'subject_name_hash':'typing.Optional[str]',
            'digest_algorithm':'typing.Optional[str]',
            'from':'typing.Optional[str]',
            'common':'typing.Optional[str]',
            'until':'typing.Optional[str]',
            'fingerprint':'typing.Optional[str]',
            'key_type':'typing.Optional[str]',
            'internal':'typing.Optional[str]',
            'lifetime':'typing.Optional[int]',
            'serial':'typing.Optional[int]',
            'key_length':'typing.Optional[int]',
            'chain':'typing.Optional[bool]',
            'CA_type_existing':'bool',
            'CA_type_internal':'bool',
            'CA_type_intermediate':'bool',
            'cert_type_existing':'bool',
            'cert_type_internal':'bool',
            'cert_type_CSR':'bool',
            'parsed':'bool',
            'can_be_revoked':'bool',
            'extensions':'dict[str]',
            'revoked_certs':'list',
            'crl_path':'str',
            'signed_certificates':'int',
    })
    CertificateEntry = typing.TypedDict('CertificateEntry', {
            'id':'int',
            'type':'int',
            'name':'str',
            'certificate':'typing.Optional[str]',
            'privatekey':'typing.Optional[str]',
            'CSR':'typing.Optional[str]',
            'acme_uri':'typing.Optional[str]',
            'domains_authenticators':'dict[str]',
            'renew_days':'int',
            'revoked_date':'typing.Optional[str]',
            'signedby':'dict[str]',
            'root_path':'str',
            'acme':'dict[str]',
            'certificate_path':'typing.Optional[str]',
            'privatekey_path':'typing.Optional[str]',
            'csr_path':'typing.Optional[str]',
            'cert_type':'str',
            'revoked':'bool',
            'expired':'typing.Optional[bool]',
            'issuer':'typing.Union[str, NoneType, dict[str]]',
            'chain_list':'list[str]',
            'country':'typing.Optional[str]',
            'state':'typing.Optional[str]',
            'city':'typing.Optional[str]',
            'organization':'typing.Optional[str]',
            'organizational_unit':'typing.Optional[str]',
            'san':'typing.Optional[list]',
            'email':'typing.Optional[str]',
            'DN':'typing.Optional[str]',
            'subject_name_hash':'typing.Optional[str]',
            'digest_algorithm':'typing.Optional[str]',
            'from':'typing.Optional[str]',
            'common':'typing.Optional[str]',
            'until':'typing.Optional[str]',
            'fingerprint':'typing.Optional[str]',
            'key_type':'typing.Optional[str]',
            'internal':'typing.Optional[str]',
            'lifetime':'typing.Optional[int]',
            'serial':'typing.Optional[int]',
            'key_length':'typing.Optional[int]',
            'chain':'typing.Optional[bool]',
            'CA_type_existing':'bool',
            'CA_type_internal':'bool',
            'CA_type_intermediate':'bool',
            'cert_type_existing':'bool',
            'cert_type_internal':'bool',
            'cert_type_CSR':'bool',
            'parsed':'bool',
            'can_be_revoked':'bool',
            'extensions':'dict[str]',
            'revoked_certs':'list',
            'crl_path':'str',
            'signed_certificates':'int',
    })
    CertificateProfiles = typing.TypedDict('CertificateProfiles', {
            'HTTPS RSA Certificate':'dict[str]',
            'HTTPS ECC Certificate':'dict[str]',
    })
    CertificateSigningRequestsProfiles = typing.TypedDict('CertificateSigningRequestsProfiles', {
            'HTTPS RSA Certificate':'dict[str]',
            'HTTPS ECC Certificate':'dict[str]',
    })
    CertificateUpdate = typing.TypedDict('CertificateUpdate', {
            'revoked':'bool',
            'renew_days':'int',
            'name':'str',
    })
    CertificateUpdateReturns = typing.TypedDict('CertificateUpdateReturns', {
            'id':'int',
            'type':'int',
            'name':'str',
            'certificate':'typing.Optional[str]',
            'privatekey':'typing.Optional[str]',
            'CSR':'typing.Optional[str]',
            'acme_uri':'typing.Optional[str]',
            'domains_authenticators':'dict[str]',
            'renew_days':'int',
            'revoked_date':'typing.Optional[str]',
            'signedby':'dict[str]',
            'root_path':'str',
            'acme':'dict[str]',
            'certificate_path':'typing.Optional[str]',
            'privatekey_path':'typing.Optional[str]',
            'csr_path':'typing.Optional[str]',
            'cert_type':'str',
            'revoked':'bool',
            'expired':'typing.Optional[bool]',
            'issuer':'typing.Union[str, NoneType, dict[str]]',
            'chain_list':'list[str]',
            'country':'typing.Optional[str]',
            'state':'typing.Optional[str]',
            'city':'typing.Optional[str]',
            'organization':'typing.Optional[str]',
            'organizational_unit':'typing.Optional[str]',
            'san':'typing.Optional[list]',
            'email':'typing.Optional[str]',
            'DN':'typing.Optional[str]',
            'subject_name_hash':'typing.Optional[str]',
            'digest_algorithm':'typing.Optional[str]',
            'from':'typing.Optional[str]',
            'common':'typing.Optional[str]',
            'until':'typing.Optional[str]',
            'fingerprint':'typing.Optional[str]',
            'key_type':'typing.Optional[str]',
            'internal':'typing.Optional[str]',
            'lifetime':'typing.Optional[int]',
            'serial':'typing.Optional[int]',
            'key_length':'typing.Optional[int]',
            'chain':'typing.Optional[bool]',
            'CA_type_existing':'bool',
            'CA_type_internal':'bool',
            'CA_type_intermediate':'bool',
            'cert_type_existing':'bool',
            'cert_type_internal':'bool',
            'cert_type_CSR':'bool',
            'parsed':'bool',
            'can_be_revoked':'bool',
            'extensions':'dict[str]',
            'revoked_certs':'list',
            'crl_path':'str',
            'signed_certificates':'int',
    })
    class CreateType(str,Enum):
        CERTIFICATECREATEINTERNAL = 'CERTIFICATE_CREATE_INTERNAL'
        CERTIFICATECREATEIMPORTED = 'CERTIFICATE_CREATE_IMPORTED'
        CERTIFICATECREATECSR = 'CERTIFICATE_CREATE_CSR'
        CERTIFICATECREATEIMPORTEDCSR = 'CERTIFICATE_CREATE_IMPORTED_CSR'
        CERTIFICATECREATEACME = 'CERTIFICATE_CREATE_ACME'
        ...
    class DigestAlgorithm(str,Enum):
        SHA224 = 'SHA224'
        SHA256 = 'SHA256'
        SHA384 = 'SHA384'
        SHA512 = 'SHA512'
        ...
    class EcCurve(str,Enum):
        SECP256R1 = 'SECP256R1'
        SECP384R1 = 'SECP384R1'
        SECP521R1 = 'SECP521R1'
        Ed25519 = 'ed25519'
        ...
    EcCurveChoices = typing.TypedDict('EcCurveChoices', {
            'SECP256R1':'typing.Literal["SECP256R1"]',
            'SECP384R1':'typing.Literal["SECP384R1"]',
            'SECP521R1':'typing.Literal["SECP521R1"]',
            'ed25519':'typing.Literal["ed25519"]',
    })
    ExtendedKeyUsage = typing.TypedDict('ExtendedKeyUsage', {
            'usages':'list[Usage]',
            'enabled':'bool',
            'extension_critical':'bool',
    })
    ExtendedKeyUsageChoices = typing.TypedDict('ExtendedKeyUsageChoices', {
            'ANY_EXTENDED_KEY_USAGE':'typing.Literal["ANY_EXTENDED_KEY_USAGE"]',
            'CERTIFICATE_TRANSPARENCY':'typing.Literal["CERTIFICATE_TRANSPARENCY"]',
            'CLIENT_AUTH':'typing.Literal["CLIENT_AUTH"]',
            'CODE_SIGNING':'typing.Literal["CODE_SIGNING"]',
            'EMAIL_PROTECTION':'typing.Literal["EMAIL_PROTECTION"]',
            'IPSEC_IKE':'typing.Literal["IPSEC_IKE"]',
            'KERBEROS_PKINIT_KDC':'typing.Literal["KERBEROS_PKINIT_KDC"]',
            'OCSP_SIGNING':'typing.Literal["OCSP_SIGNING"]',
            'SERVER_AUTH':'typing.Literal["SERVER_AUTH"]',
            'SMARTCARD_LOGON':'typing.Literal["SMARTCARD_LOGON"]',
            'TIME_STAMPING':'typing.Literal["TIME_STAMPING"]',
    })
    class KeyType(str,Enum):
        RSA = 'RSA'
        EC = 'EC'
        ...
    KeyUsage = typing.TypedDict('KeyUsage', {
            'enabled':'bool',
            'digital_signature':'bool',
            'content_commitment':'bool',
            'key_encipherment':'bool',
            'data_encipherment':'bool',
            'key_agreement':'bool',
            'key_cert_sign':'bool',
            'crl_sign':'bool',
            'encipher_only':'bool',
            'decipher_only':'bool',
            'extension_critical':'bool',
    })
    PrivateKeyTypeChoices = typing.TypedDict('PrivateKeyTypeChoices', {
            'RSA':'typing.Literal["RSA"]',
            'EC':'typing.Literal["EC"]',
    })
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
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
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
    class Usage(str,Enum):
        ANYEXTENDEDKEYUSAGE = 'ANY_EXTENDED_KEY_USAGE'
        CERTIFICATETRANSPARENCY = 'CERTIFICATE_TRANSPARENCY'
        CLIENTAUTH = 'CLIENT_AUTH'
        CODESIGNING = 'CODE_SIGNING'
        EMAILPROTECTION = 'EMAIL_PROTECTION'
        IPSECIKE = 'IPSEC_IKE'
        KERBEROSPKINITKDC = 'KERBEROS_PKINIT_KDC'
        OCSPSIGNING = 'OCSP_SIGNING'
        SERVERAUTH = 'SERVER_AUTH'
        SMARTCARDLOGON = 'SMARTCARD_LOGON'
        TIMESTAMPING = 'TIME_STAMPING'
        ...
