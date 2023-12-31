
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
from enum import Enum

class AuthTwofactor(ConfigMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'auth.twofactor')

    AuthTwofactorEntry = typing.TypedDict('AuthTwofactorEntry', {
            'enabled':'bool',
            'otp_digits':'int',
            'window':'int',
            'interval':'int',
            'services':'Services',
            'id':'int',
    })
    AuthTwofactorUpdate = typing.TypedDict('AuthTwofactorUpdate', {
            'enabled':'bool',
            'otp_digits':'int',
            'window':'int',
            'interval':'int',
            'services':'Services',
    })
    AuthTwofactorUpdateReturns = typing.TypedDict('AuthTwofactorUpdateReturns', {
            'enabled':'bool',
            'otp_digits':'int',
            'window':'int',
            'interval':'int',
            'services':'Services',
            'id':'int',
    })
    Services = typing.TypedDict('Services', {
            'ssh':'bool',
    })
