
from pytruenas.base import Namespace

import typing
from enum import Enum

class Certificate(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'certificate')

    CertificateSigningRequestsProfiles = typing.TypedDict('CertificateSigningRequestsProfiles', {
            'HTTPS RSA Certificate':'dict[str]',
            'HTTPS ECC Certificate':'dict[str]',
    })
    class EcCurve(str,Enum):
        SECP256R1 = 'SECP256R1'
        SECP384R1 = 'SECP384R1'
        SECP521R1 = 'SECP521R1'
        Ed25519 = 'ed25519'
        ...
    class KeyType(str,Enum):
        RSA = 'RSA'
        EC = 'EC'
        ...
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
    BasicConstraints = typing.TypedDict('BasicConstraints', {
            'ca':'bool',
            'enabled':'bool',
            'path_length':'typing.Optional[int]',
            'extension_critical':'bool',
    })
    AuthorityKeyIdentifier = typing.TypedDict('AuthorityKeyIdentifier', {
            'authority_cert_issuer':'bool',
            'enabled':'bool',
            'extension_critical':'bool',
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
    ExtendedKeyUsage = typing.TypedDict('ExtendedKeyUsage', {
            'usages':'list[Usage]',
            'enabled':'bool',
            'extension_critical':'bool',
    })
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
            'san':'typing.Optional[list[str]]',
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
    class SECP256R1(str,Enum):
        SECP256R1 = 'SECP256R1'
        ...
    class SECP384R1(str,Enum):
        SECP384R1 = 'SECP384R1'
        ...
    class SECP521R1(str,Enum):
        SECP521R1 = 'SECP521R1'
        ...
    class Ed25519(str,Enum):
        Ed25519 = 'ed25519'
        ...
    EcCurveChoices = typing.TypedDict('EcCurveChoices', {
            'SECP256R1':'SECP256R1',
            'SECP384R1':'SECP384R1',
            'SECP521R1':'SECP521R1',
            'ed25519':'Ed25519',
    })
    class ANYEXTENDEDKEYUSAGE(str,Enum):
        ANYEXTENDEDKEYUSAGE = 'ANY_EXTENDED_KEY_USAGE'
        ...
    class CERTIFICATETRANSPARENCY(str,Enum):
        CERTIFICATETRANSPARENCY = 'CERTIFICATE_TRANSPARENCY'
        ...
    class CLIENTAUTH(str,Enum):
        CLIENTAUTH = 'CLIENT_AUTH'
        ...
    class CODESIGNING(str,Enum):
        CODESIGNING = 'CODE_SIGNING'
        ...
    class EMAILPROTECTION(str,Enum):
        EMAILPROTECTION = 'EMAIL_PROTECTION'
        ...
    class IPSECIKE(str,Enum):
        IPSECIKE = 'IPSEC_IKE'
        ...
    class KERBEROSPKINITKDC(str,Enum):
        KERBEROSPKINITKDC = 'KERBEROS_PKINIT_KDC'
        ...
    class OCSPSIGNING(str,Enum):
        OCSPSIGNING = 'OCSP_SIGNING'
        ...
    class SERVERAUTH(str,Enum):
        SERVERAUTH = 'SERVER_AUTH'
        ...
    class SMARTCARDLOGON(str,Enum):
        SMARTCARDLOGON = 'SMARTCARD_LOGON'
        ...
    class TIMESTAMPING(str,Enum):
        TIMESTAMPING = 'TIME_STAMPING'
        ...
    ExtendedKeyUsageChoices = typing.TypedDict('ExtendedKeyUsageChoices', {
            'ANY_EXTENDED_KEY_USAGE':'ANYEXTENDEDKEYUSAGE',
            'CERTIFICATE_TRANSPARENCY':'CERTIFICATETRANSPARENCY',
            'CLIENT_AUTH':'CLIENTAUTH',
            'CODE_SIGNING':'CODESIGNING',
            'EMAIL_PROTECTION':'EMAILPROTECTION',
            'IPSEC_IKE':'IPSECIKE',
            'KERBEROS_PKINIT_KDC':'KERBEROSPKINITKDC',
            'OCSP_SIGNING':'OCSPSIGNING',
            'SERVER_AUTH':'SERVERAUTH',
            'SMARTCARD_LOGON':'SMARTCARDLOGON',
            'TIME_STAMPING':'TIMESTAMPING',
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
    class RSA(str,Enum):
        RSA = 'RSA'
        ...
    class EC(str,Enum):
        EC = 'EC'
        ...
    PrivateKeyTypeChoices = typing.TypedDict('PrivateKeyTypeChoices', {
            'RSA':'RSA',
            'EC':'EC',
    })
    CertificateProfiles = typing.TypedDict('CertificateProfiles', {
            'HTTPS RSA Certificate':'dict[str]',
            'HTTPS ECC Certificate':'dict[str]',
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
            'san':'typing.Optional[list[str]]',
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
    CertificateEntry_ = typing.TypedDict('CertificateEntry_', {
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
            'san':'typing.Optional[list[str]]',
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
    CertificateEntry__ = typing.TypedDict('CertificateEntry__', {
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
            'san':'typing.Optional[list[str]]',
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
            'san':'typing.Optional[list[str]]',
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
