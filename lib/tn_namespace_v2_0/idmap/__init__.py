
from pytruenas import Namespace
import typing
class Idmap(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'idmap')

    IdmapAdOptions = typing.TypedDict('IdmapAdOptions', {
            'schema_mode':'str',
            'unix_primary_group':'bool',
            'unix_nss_info':'bool',
    })
    IdmapAutoridOptions = typing.TypedDict('IdmapAutoridOptions', {
            'rangesize':'int',
            'readonly':'bool',
            'ignore_builtin':'bool',
    })
    IdmapLdapOptions = typing.TypedDict('IdmapLdapOptions', {
            'ldap_base_dn':'str',
            'ldap_user_dn':'str',
            'ldap_user_dn_password':'str',
            'ldap_url':'str',
            'readonly':'bool',
            'ssl':'str',
            'validate_certificates':'bool',
    })
    IdmapNssOptions = typing.TypedDict('IdmapNssOptions', {
            'linked_service':'str',
    })
    IdmapRfc2307Options = typing.TypedDict('IdmapRfc2307Options', {
            'ldap_server':'str',
            'ldap_realm':'bool',
            'bind_path_user':'str',
            'bind_path_group':'str',
            'user_cn':'bool',
            'cn_realm':'str',
            'ldap_domain':'str',
            'ldap_url':'str',
            'ldap_user_dn':'str',
            'ldap_user_dn_password':'str',
            'ssl':'str',
            'validate_certificates':'bool',
    })
    IdmapRidOptions = typing.TypedDict('IdmapRidOptions', {
            'sssd_compat':'bool',
    })
    IdmapDomainCreate = typing.TypedDict('IdmapDomainCreate', {
            'name':'str',
            'dns_domain_name':'str',
            'range_low':'int',
            'range_high':'int',
            'idmap_backend':'str',
            'certificate':'typing.Optional[int]',
            'options':'typing.Union[ForwardRef(IdmapAdOptions), ForwardRef(IdmapAutoridOptions), ForwardRef(IdmapLdapOptions), ForwardRef(IdmapNssOptions), ForwardRef(IdmapRfc2307Options), ForwardRef(IdmapRidOptions), dict[str]]',
    })
    IdmapAdOptions_ = typing.TypedDict('IdmapAdOptions_', {
            'schema_mode':'str',
            'unix_primary_group':'bool',
            'unix_nss_info':'bool',
    })
    IdmapAutoridOptions_ = typing.TypedDict('IdmapAutoridOptions_', {
            'rangesize':'int',
            'readonly':'bool',
            'ignore_builtin':'bool',
    })
    IdmapLdapOptions_ = typing.TypedDict('IdmapLdapOptions_', {
            'ldap_base_dn':'str',
            'ldap_user_dn':'str',
            'ldap_user_dn_password':'str',
            'ldap_url':'str',
            'readonly':'bool',
            'ssl':'str',
            'validate_certificates':'bool',
    })
    IdmapNssOptions_ = typing.TypedDict('IdmapNssOptions_', {
            'linked_service':'str',
    })
    IdmapRfc2307Options_ = typing.TypedDict('IdmapRfc2307Options_', {
            'ldap_server':'str',
            'ldap_realm':'bool',
            'bind_path_user':'str',
            'bind_path_group':'str',
            'user_cn':'bool',
            'cn_realm':'str',
            'ldap_domain':'str',
            'ldap_url':'str',
            'ldap_user_dn':'str',
            'ldap_user_dn_password':'str',
            'ssl':'str',
            'validate_certificates':'bool',
    })
    IdmapRidOptions_ = typing.TypedDict('IdmapRidOptions_', {
            'sssd_compat':'bool',
    })
    IdmapCreateReturns = typing.TypedDict('IdmapCreateReturns', {
            'name':'str',
            'dns_domain_name':'str',
            'range_low':'int',
            'range_high':'int',
            'idmap_backend':'str',
            'certificate':'typing.Optional[int]',
            'options':'typing.Union[ForwardRef(IdmapAdOptions_), ForwardRef(IdmapAutoridOptions_), ForwardRef(IdmapLdapOptions_), ForwardRef(IdmapNssOptions_), ForwardRef(IdmapRfc2307Options_), ForwardRef(IdmapRidOptions_), dict[str]]',
            'id':'int',
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
    IdmapAdOptions__ = typing.TypedDict('IdmapAdOptions__', {
            'schema_mode':'str',
            'unix_primary_group':'bool',
            'unix_nss_info':'bool',
    })
    IdmapAutoridOptions__ = typing.TypedDict('IdmapAutoridOptions__', {
            'rangesize':'int',
            'readonly':'bool',
            'ignore_builtin':'bool',
    })
    IdmapLdapOptions__ = typing.TypedDict('IdmapLdapOptions__', {
            'ldap_base_dn':'str',
            'ldap_user_dn':'str',
            'ldap_user_dn_password':'str',
            'ldap_url':'str',
            'readonly':'bool',
            'ssl':'str',
            'validate_certificates':'bool',
    })
    IdmapNssOptions__ = typing.TypedDict('IdmapNssOptions__', {
            'linked_service':'str',
    })
    IdmapRfc2307Options__ = typing.TypedDict('IdmapRfc2307Options__', {
            'ldap_server':'str',
            'ldap_realm':'bool',
            'bind_path_user':'str',
            'bind_path_group':'str',
            'user_cn':'bool',
            'cn_realm':'str',
            'ldap_domain':'str',
            'ldap_url':'str',
            'ldap_user_dn':'str',
            'ldap_user_dn_password':'str',
            'ssl':'str',
            'validate_certificates':'bool',
    })
    IdmapRidOptions__ = typing.TypedDict('IdmapRidOptions__', {
            'sssd_compat':'bool',
    })
    IdmapDomainEntry = typing.TypedDict('IdmapDomainEntry', {
            'name':'str',
            'dns_domain_name':'str',
            'range_low':'int',
            'range_high':'int',
            'idmap_backend':'str',
            'certificate':'typing.Optional[int]',
            'options':'typing.Union[ForwardRef(IdmapAdOptions__), ForwardRef(IdmapAutoridOptions__), ForwardRef(IdmapLdapOptions__), ForwardRef(IdmapNssOptions__), ForwardRef(IdmapRfc2307Options__), ForwardRef(IdmapRidOptions__), dict[str]]',
            'id':'int',
    })
    IdmapAdOptions___ = typing.TypedDict('IdmapAdOptions___', {
            'schema_mode':'str',
            'unix_primary_group':'bool',
            'unix_nss_info':'bool',
    })
    IdmapAutoridOptions___ = typing.TypedDict('IdmapAutoridOptions___', {
            'rangesize':'int',
            'readonly':'bool',
            'ignore_builtin':'bool',
    })
    IdmapLdapOptions___ = typing.TypedDict('IdmapLdapOptions___', {
            'ldap_base_dn':'str',
            'ldap_user_dn':'str',
            'ldap_user_dn_password':'str',
            'ldap_url':'str',
            'readonly':'bool',
            'ssl':'str',
            'validate_certificates':'bool',
    })
    IdmapNssOptions___ = typing.TypedDict('IdmapNssOptions___', {
            'linked_service':'str',
    })
    IdmapRfc2307Options___ = typing.TypedDict('IdmapRfc2307Options___', {
            'ldap_server':'str',
            'ldap_realm':'bool',
            'bind_path_user':'str',
            'bind_path_group':'str',
            'user_cn':'bool',
            'cn_realm':'str',
            'ldap_domain':'str',
            'ldap_url':'str',
            'ldap_user_dn':'str',
            'ldap_user_dn_password':'str',
            'ssl':'str',
            'validate_certificates':'bool',
    })
    IdmapRidOptions___ = typing.TypedDict('IdmapRidOptions___', {
            'sssd_compat':'bool',
    })
    IdmapDomainEntry_ = typing.TypedDict('IdmapDomainEntry_', {
            'name':'str',
            'dns_domain_name':'str',
            'range_low':'int',
            'range_high':'int',
            'idmap_backend':'str',
            'certificate':'typing.Optional[int]',
            'options':'typing.Union[ForwardRef(IdmapAdOptions___), ForwardRef(IdmapAutoridOptions___), ForwardRef(IdmapLdapOptions___), ForwardRef(IdmapNssOptions___), ForwardRef(IdmapRfc2307Options___), ForwardRef(IdmapRidOptions___), dict[str]]',
            'id':'int',
    })
    IdmapAdOptions____ = typing.TypedDict('IdmapAdOptions____', {
            'schema_mode':'str',
            'unix_primary_group':'bool',
            'unix_nss_info':'bool',
    })
    IdmapAutoridOptions____ = typing.TypedDict('IdmapAutoridOptions____', {
            'rangesize':'int',
            'readonly':'bool',
            'ignore_builtin':'bool',
    })
    IdmapLdapOptions____ = typing.TypedDict('IdmapLdapOptions____', {
            'ldap_base_dn':'str',
            'ldap_user_dn':'str',
            'ldap_user_dn_password':'str',
            'ldap_url':'str',
            'readonly':'bool',
            'ssl':'str',
            'validate_certificates':'bool',
    })
    IdmapNssOptions____ = typing.TypedDict('IdmapNssOptions____', {
            'linked_service':'str',
    })
    IdmapRfc2307Options____ = typing.TypedDict('IdmapRfc2307Options____', {
            'ldap_server':'str',
            'ldap_realm':'bool',
            'bind_path_user':'str',
            'bind_path_group':'str',
            'user_cn':'bool',
            'cn_realm':'str',
            'ldap_domain':'str',
            'ldap_url':'str',
            'ldap_user_dn':'str',
            'ldap_user_dn_password':'str',
            'ssl':'str',
            'validate_certificates':'bool',
    })
    IdmapRidOptions____ = typing.TypedDict('IdmapRidOptions____', {
            'sssd_compat':'bool',
    })
    IdmapDomainEntry__ = typing.TypedDict('IdmapDomainEntry__', {
            'name':'str',
            'dns_domain_name':'str',
            'range_low':'int',
            'range_high':'int',
            'idmap_backend':'str',
            'certificate':'typing.Optional[int]',
            'options':'typing.Union[ForwardRef(IdmapAdOptions____), ForwardRef(IdmapAutoridOptions____), ForwardRef(IdmapLdapOptions____), ForwardRef(IdmapNssOptions____), ForwardRef(IdmapRfc2307Options____), ForwardRef(IdmapRidOptions____), dict[str]]',
            'id':'int',
    })
    IdmapAdOptions_____ = typing.TypedDict('IdmapAdOptions_____', {
            'schema_mode':'str',
            'unix_primary_group':'bool',
            'unix_nss_info':'bool',
    })
    IdmapAutoridOptions_____ = typing.TypedDict('IdmapAutoridOptions_____', {
            'rangesize':'int',
            'readonly':'bool',
            'ignore_builtin':'bool',
    })
    IdmapLdapOptions_____ = typing.TypedDict('IdmapLdapOptions_____', {
            'ldap_base_dn':'str',
            'ldap_user_dn':'str',
            'ldap_user_dn_password':'str',
            'ldap_url':'str',
            'readonly':'bool',
            'ssl':'str',
            'validate_certificates':'bool',
    })
    IdmapNssOptions_____ = typing.TypedDict('IdmapNssOptions_____', {
            'linked_service':'str',
    })
    IdmapRfc2307Options_____ = typing.TypedDict('IdmapRfc2307Options_____', {
            'ldap_server':'str',
            'ldap_realm':'bool',
            'bind_path_user':'str',
            'bind_path_group':'str',
            'user_cn':'bool',
            'cn_realm':'str',
            'ldap_domain':'str',
            'ldap_url':'str',
            'ldap_user_dn':'str',
            'ldap_user_dn_password':'str',
            'ssl':'str',
            'validate_certificates':'bool',
    })
    IdmapRidOptions_____ = typing.TypedDict('IdmapRidOptions_____', {
            'sssd_compat':'bool',
    })
    IdmapUpdate = typing.TypedDict('IdmapUpdate', {
            'name':'str',
            'dns_domain_name':'str',
            'range_low':'int',
            'range_high':'int',
            'idmap_backend':'str',
            'certificate':'typing.Optional[int]',
            'options':'typing.Union[ForwardRef(IdmapAdOptions_____), ForwardRef(IdmapAutoridOptions_____), ForwardRef(IdmapLdapOptions_____), ForwardRef(IdmapNssOptions_____), ForwardRef(IdmapRfc2307Options_____), ForwardRef(IdmapRidOptions_____), dict[str]]',
    })
    IdmapAdOptions______ = typing.TypedDict('IdmapAdOptions______', {
            'schema_mode':'str',
            'unix_primary_group':'bool',
            'unix_nss_info':'bool',
    })
    IdmapAutoridOptions______ = typing.TypedDict('IdmapAutoridOptions______', {
            'rangesize':'int',
            'readonly':'bool',
            'ignore_builtin':'bool',
    })
    IdmapLdapOptions______ = typing.TypedDict('IdmapLdapOptions______', {
            'ldap_base_dn':'str',
            'ldap_user_dn':'str',
            'ldap_user_dn_password':'str',
            'ldap_url':'str',
            'readonly':'bool',
            'ssl':'str',
            'validate_certificates':'bool',
    })
    IdmapNssOptions______ = typing.TypedDict('IdmapNssOptions______', {
            'linked_service':'str',
    })
    IdmapRfc2307Options______ = typing.TypedDict('IdmapRfc2307Options______', {
            'ldap_server':'str',
            'ldap_realm':'bool',
            'bind_path_user':'str',
            'bind_path_group':'str',
            'user_cn':'bool',
            'cn_realm':'str',
            'ldap_domain':'str',
            'ldap_url':'str',
            'ldap_user_dn':'str',
            'ldap_user_dn_password':'str',
            'ssl':'str',
            'validate_certificates':'bool',
    })
    IdmapRidOptions______ = typing.TypedDict('IdmapRidOptions______', {
            'sssd_compat':'bool',
    })
    IdmapUpdateReturns = typing.TypedDict('IdmapUpdateReturns', {
            'name':'str',
            'dns_domain_name':'str',
            'range_low':'int',
            'range_high':'int',
            'idmap_backend':'str',
            'certificate':'typing.Optional[int]',
            'options':'typing.Union[ForwardRef(IdmapAdOptions______), ForwardRef(IdmapAutoridOptions______), ForwardRef(IdmapLdapOptions______), ForwardRef(IdmapNssOptions______), ForwardRef(IdmapRfc2307Options______), ForwardRef(IdmapRidOptions______), dict[str]]',
            'id':'int',
    })
