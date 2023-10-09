
from pytruenas.base import Namespace

import typing
from enum import Enum

class Idmap(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'idmap')

    class IdmapBackend(str,Enum):
        AD = 'AD'
        AUTORID = 'AUTORID'
        LDAP = 'LDAP'
        NSS = 'NSS'
        RFC2307 = 'RFC2307'
        RID = 'RID'
        TDB = 'TDB'
        ...
    class NssInfoAd(str,Enum):
        SFU = 'SFU'
        SFU20 = 'SFU20'
        RFC2307 = 'RFC2307'
        ...
    IdmapAdOptions = typing.TypedDict('IdmapAdOptions', {
            'schema_mode':'NssInfoAd',
            'unix_primary_group':'bool',
            'unix_nss_info':'bool',
    })
    IdmapAutoridOptions = typing.TypedDict('IdmapAutoridOptions', {
            'rangesize':'int',
            'readonly':'bool',
            'ignore_builtin':'bool',
    })
    class LdapSslChoice(str,Enum):
        OFF = 'OFF'
        ON = 'ON'
        STARTTLS = 'START_TLS'
        ...
    IdmapLdapOptions = typing.TypedDict('IdmapLdapOptions', {
            'ldap_base_dn':'str',
            'ldap_user_dn':'str',
            'ldap_user_dn_password':'str',
            'ldap_url':'str',
            'readonly':'bool',
            'ssl':'LdapSslChoice',
            'validate_certificates':'bool',
    })
    class LinkedService(str,Enum):
        LOCALACCOUNT = 'LOCAL_ACCOUNT'
        LDAP = 'LDAP'
        ...
    IdmapNssOptions = typing.TypedDict('IdmapNssOptions', {
            'linked_service':'LinkedService',
    })
    class LdapServer(str,Enum):
        AD = 'AD'
        STANDALONE = 'STANDALONE'
        ...
    IdmapRfc2307Options = typing.TypedDict('IdmapRfc2307Options', {
            'ldap_server':'LdapServer',
            'ldap_realm':'bool',
            'bind_path_user':'str',
            'bind_path_group':'str',
            'user_cn':'bool',
            'cn_realm':'str',
            'ldap_domain':'str',
            'ldap_url':'str',
            'ldap_user_dn':'str',
            'ldap_user_dn_password':'str',
            'ssl':'LdapSslChoice',
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
            'idmap_backend':'IdmapBackend',
            'certificate':'typing.Optional[int]',
            'options':'typing.Union[IdmapAdOptions, IdmapAutoridOptions, IdmapLdapOptions, IdmapNssOptions, IdmapRfc2307Options, IdmapRidOptions, dict[str]]',
    })
    IdmapCreateReturns = typing.TypedDict('IdmapCreateReturns', {
            'name':'str',
            'dns_domain_name':'str',
            'range_low':'int',
            'range_high':'int',
            'idmap_backend':'IdmapBackend',
            'certificate':'typing.Optional[int]',
            'options':'typing.Union[IdmapAdOptions, IdmapAutoridOptions, IdmapLdapOptions, IdmapNssOptions, IdmapRfc2307Options, IdmapRidOptions, dict[str]]',
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
    IdmapDomainEntry = typing.TypedDict('IdmapDomainEntry', {
            'name':'str',
            'dns_domain_name':'str',
            'range_low':'int',
            'range_high':'int',
            'idmap_backend':'IdmapBackend',
            'certificate':'typing.Optional[int]',
            'options':'typing.Union[IdmapAdOptions, IdmapAutoridOptions, IdmapLdapOptions, IdmapNssOptions, IdmapRfc2307Options, IdmapRidOptions, dict[str]]',
            'id':'int',
    })
    IdmapDomainEntry_ = typing.TypedDict('IdmapDomainEntry_', {
            'name':'str',
            'dns_domain_name':'str',
            'range_low':'int',
            'range_high':'int',
            'idmap_backend':'IdmapBackend',
            'certificate':'typing.Optional[int]',
            'options':'typing.Union[IdmapAdOptions, IdmapAutoridOptions, IdmapLdapOptions, IdmapNssOptions, IdmapRfc2307Options, IdmapRidOptions, dict[str]]',
            'id':'int',
    })
    IdmapDomainEntry__ = typing.TypedDict('IdmapDomainEntry__', {
            'name':'str',
            'dns_domain_name':'str',
            'range_low':'int',
            'range_high':'int',
            'idmap_backend':'IdmapBackend',
            'certificate':'typing.Optional[int]',
            'options':'typing.Union[IdmapAdOptions, IdmapAutoridOptions, IdmapLdapOptions, IdmapNssOptions, IdmapRfc2307Options, IdmapRidOptions, dict[str]]',
            'id':'int',
    })
    IdmapUpdate = typing.TypedDict('IdmapUpdate', {
            'name':'str',
            'dns_domain_name':'str',
            'range_low':'int',
            'range_high':'int',
            'idmap_backend':'IdmapBackend',
            'certificate':'typing.Optional[int]',
            'options':'typing.Union[IdmapAdOptions, IdmapAutoridOptions, IdmapLdapOptions, IdmapNssOptions, IdmapRfc2307Options, IdmapRidOptions, dict[str]]',
    })
    IdmapUpdateReturns = typing.TypedDict('IdmapUpdateReturns', {
            'name':'str',
            'dns_domain_name':'str',
            'range_low':'int',
            'range_high':'int',
            'idmap_backend':'IdmapBackend',
            'certificate':'typing.Optional[int]',
            'options':'typing.Union[IdmapAdOptions, IdmapAutoridOptions, IdmapLdapOptions, IdmapNssOptions, IdmapRfc2307Options, IdmapRidOptions, dict[str]]',
            'id':'int',
    })
