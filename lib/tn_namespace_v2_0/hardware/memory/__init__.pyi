
from pytruenas import Namespace, TrueNASClient
import typing
class HardwareMemory(Namespace):
    _namespace:typing.Literal['hardware.memory']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
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

