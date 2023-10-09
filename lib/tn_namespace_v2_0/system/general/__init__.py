
from pytruenas.base import Namespace

import typing
class SystemGeneral(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'system.general')

    UiCertificate = typing.TypedDict('UiCertificate', {
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
    SystemGeneralEntry = typing.TypedDict('SystemGeneralEntry', {
            'ui_certificate':'UiCertificate',
            'ui_httpsport':'int',
            'ui_httpsredirect':'bool',
            'ui_httpsprotocols':'list[str]',
            'ui_port':'int',
            'ui_address':'list[str]',
            'ui_v6address':'list[str]',
            'ui_allowlist':'list[str]',
            'ui_consolemsg':'bool',
            'ui_x_frame_options':'str',
            'kbdmap':'str',
            'language':'str',
            'timezone':'str',
            'usage_collection':'typing.Optional[bool]',
            'birthday':'str',
            'wizardshown':'bool',
            'usage_collection_is_set':'bool',
            'ds_auth':'bool',
            'id':'int',
    })
    UIHTTPSProtocolChoices = typing.TypedDict('UIHTTPSProtocolChoices', {
            'TLSv1':'str',
            'TLSv1.1':'str',
            'TLSv1.2':'str',
            'TLSv1.3':'str',
    })
    GeneralSettings = typing.TypedDict('GeneralSettings', {
            'ui_httpsport':'int',
            'ui_httpsredirect':'bool',
            'ui_httpsprotocols':'list[str]',
            'ui_port':'int',
            'ui_address':'list[str]',
            'ui_v6address':'list[str]',
            'ui_allowlist':'list[str]',
            'ui_consolemsg':'bool',
            'ui_x_frame_options':'str',
            'kbdmap':'str',
            'language':'str',
            'timezone':'str',
            'usage_collection':'typing.Optional[bool]',
            'birthday':'str',
            'ds_auth':'bool',
            'ui_certificate':'typing.Optional[int]',
            'rollback_timeout':'typing.Optional[int]',
            'ui_restart_delay':'typing.Optional[int]',
    })
    UiCertificate_ = typing.TypedDict('UiCertificate_', {
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
    SystemGeneralUpdateReturns = typing.TypedDict('SystemGeneralUpdateReturns', {
            'ui_certificate':'UiCertificate_',
            'ui_httpsport':'int',
            'ui_httpsredirect':'bool',
            'ui_httpsprotocols':'list[str]',
            'ui_port':'int',
            'ui_address':'list[str]',
            'ui_v6address':'list[str]',
            'ui_allowlist':'list[str]',
            'ui_consolemsg':'bool',
            'ui_x_frame_options':'str',
            'kbdmap':'str',
            'language':'str',
            'timezone':'str',
            'usage_collection':'typing.Optional[bool]',
            'birthday':'str',
            'wizardshown':'bool',
            'usage_collection_is_set':'bool',
            'ds_auth':'bool',
            'id':'int',
    })
