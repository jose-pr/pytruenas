
from pytruenas.base import Namespace

import typing
from enum import Enum

class SystemSecurity(Namespace):
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
