
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

class AuthTwofactorEntry(typing.TypedDict):
        enabled:'bool'
        otp_digits:'int'
        window:'int'
        interval:'int'
        services:'Services'
        id:'int'
        ...
class Services(typing.TypedDict):
        ssh:'bool'
        ...
class AuthTwofactorUpdate(typing.TypedDict):
        enabled:'bool'
        otp_digits:'int'
        window:'int'
        interval:'int'
        services:'Services'
        ...
class AuthTwofactorUpdateReturns(typing.TypedDict):
        enabled:'bool'
        otp_digits:'int'
        window:'int'
        interval:'int'
        services:'Services'
        id:'int'
        ...
