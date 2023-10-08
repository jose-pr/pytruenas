
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Ipmi(Namespace):
    _namespace:_ty.Literal['ipmi']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def is_loaded(self, 
    /) -> 'bool': 
        """
        Returns a boolean value indicating if /dev/ipmi0 is loaded.

        Parameters
        ----------
        Returns
        -------
        bool:
            ipmi_loaded
        """
        ...
