
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class AuthTwofactor(Namespace):
    _namespace:_ty.Literal['auth.twofactor']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def config(self, 
    /) -> 'dict[str]': 
        """
        

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            auth_twofactor_entry
        """
        ...
    @_ty.overload
    def update(self, 
        auth_twofactor_update:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            auth_twofactor_update_returns
        """
        ...
