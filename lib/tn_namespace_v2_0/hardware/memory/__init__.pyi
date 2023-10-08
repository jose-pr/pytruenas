
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class HardwareMemory(Namespace):
    _namespace:_ty.Literal['hardware.memory']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def error_info(self, 
    /) -> 'dict[str]': 
        """
        

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            mem_ctrl
        """
        ...
