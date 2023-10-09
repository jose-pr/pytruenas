
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
class SystemSecurity(ConfigMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'system.security')

    SystemSecurityEntry = typing.TypedDict('SystemSecurityEntry', {
            'enable_fips':'bool',
            'id':'int',
    })
    SystemSecurityUpdate = typing.TypedDict('SystemSecurityUpdate', {
            'enable_fips':'bool',
    })
    SystemSecurityUpdateReturns = typing.TypedDict('SystemSecurityUpdateReturns', {
            'enable_fips':'bool',
            'id':'int',
    })
