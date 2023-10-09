
from pytruenas import Namespace, TrueNASClient
import typing
class AuthTwofactor(Namespace):
    _namespace:typing.Literal['auth.twofactor']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def config(self, 
    /) -> 'AuthTwofactorEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        AuthTwofactorEntry:
            auth_twofactor_entry
        """
        ...
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
    @typing.overload
    def update(self, 
        auth_twofactor_update:'AuthTwofactorUpdate'={},
    /) -> 'AuthTwofactorUpdateReturns': 
        """
        `otp_digits` represents number of allowed digits in the OTP.
        
        `window` extends the validity to `window` many counter ticks before and after the current one.
        
        `interval` is time duration in seconds specifying OTP expiration time from it's creation time.

        Parameters
        ----------
        auth_twofactor_update:
            auth_twofactor_update
        Returns
        -------
        AuthTwofactorUpdateReturns:
            auth_twofactor_update_returns
        """
        ...
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

