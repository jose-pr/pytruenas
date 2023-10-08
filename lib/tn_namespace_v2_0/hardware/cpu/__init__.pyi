
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class HardwareCpu(Namespace):
    _namespace:_ty.Literal['hardware.cpu']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def available_governors(self, 
    /) -> 'dict[str]': 
        """
        Return available cpu governors

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            governor
        """
        ...
    @_ty.overload
    def current_governor(self, 
    /) -> 'str': 
        """
        Returns currently set cpu governor

        Parameters
        ----------
        Returns
        -------
        str:
            governor
        """
        ...
    @_ty.overload
    def set_governor(self, 
        governor:'str',
    /) -> None: 
        """
        Set the cpu governor to `governor` on all cpus

        Parameters
        ----------
        governor:
            governor
        Returns
        -------
        """
        ...
