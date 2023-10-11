
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin
from enum import Enum
import typing
class AuthTwofactor(
    ConfigMixin,
    Namespace
    ):
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
    @typing.overload
    def update(self, 
        auth_twofactor_update:'AuthTwofactorUpdate',
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
    AuthTwofactorEntry = typing.TypedDict('AuthTwofactorEntry', {
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
