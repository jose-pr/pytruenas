
from pytruenas import Namespace, TrueNASClient
import typing
class HardwareCpu(Namespace):
    _namespace:typing.Literal['hardware.cpu']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
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
    @typing.overload
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
    @typing.overload
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

