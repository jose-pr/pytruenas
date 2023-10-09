
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
class AcmeDnsAuthenticator(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'acme.dns.authenticator')

    AttributeSchema = typing.TypedDict('AttributeSchema', {
            '_name_':'str',
            'title':'str',
            '_required_':'bool',
    })
    AuthenticatorSchema = typing.TypedDict('AuthenticatorSchema', {
            'key':'str',
            'schema':'list[AttributeSchema]',
    })
    AcmeDnsAuthenticatorCreate = typing.TypedDict('AcmeDnsAuthenticatorCreate', {
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorCreateReturns = typing.TypedDict('AcmeDnsAuthenticatorCreateReturns', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
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
    AcmeDnsAuthenticatorEntry = typing.TypedDict('AcmeDnsAuthenticatorEntry', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    DnsAuthenticatorUpdate = typing.TypedDict('DnsAuthenticatorUpdate', {
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorUpdateReturns = typing.TypedDict('AcmeDnsAuthenticatorUpdateReturns', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
