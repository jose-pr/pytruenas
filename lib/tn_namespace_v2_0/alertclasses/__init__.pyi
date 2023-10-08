
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Alertclasses(Namespace):
    _namespace:_ty.Literal['alertclasses']
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
            alertclasses_entry
        """
        ...
    @_ty.overload
    def update(self, 
        alertclasses_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update default Alert settings.

        Parameters
        ----------
        alertclasses_update:
            alertclasses_update
        Returns
        -------
        dict[str]:
            alertclasses_update_returns
        """
        ...
