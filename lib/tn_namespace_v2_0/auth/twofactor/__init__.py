
from pytruenas import Namespace
import typing
class AuthTwofactor(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'auth.twofactor')

    Services = typing.TypedDict('Services', {
            'ssh':'bool',
    })
    AuthTwofactorEntry = typing.TypedDict('AuthTwofactorEntry', {
            'enabled':'bool',
            'otp_digits':'int',
            'window':'int',
            'interval':'int',
            'services':'Services',
            'id':'int',
    })
    Services_ = typing.TypedDict('Services_', {
            'ssh':'bool',
    })
    AuthTwofactorUpdate = typing.TypedDict('AuthTwofactorUpdate', {
            'enabled':'bool',
            'otp_digits':'int',
            'window':'int',
            'interval':'int',
            'services':'Services_',
    })
    Services__ = typing.TypedDict('Services__', {
            'ssh':'bool',
    })
    AuthTwofactorUpdateReturns = typing.TypedDict('AuthTwofactorUpdateReturns', {
            'enabled':'bool',
            'otp_digits':'int',
            'window':'int',
            'interval':'int',
            'services':'Services__',
            'id':'int',
    })
