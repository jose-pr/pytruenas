
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Ipmi(
    Namespace
    ):
    _namespace:typing.Literal['ipmi']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
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
