
from pytruenas import Namespace, TrueNASClient
import typing
class Alertclasses(Namespace):
    _namespace:typing.Literal['alertclasses']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def config(self, 
    /) -> 'AlertclassesEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        AlertclassesEntry:
            alertclasses_entry
        """
        ...
    @typing.overload
    def update(self, 
        alertclasses_update:'AlertclassesUpdate'={},
    /) -> 'AlertclassesUpdateReturns': 
        """
        Update default Alert settings.

        Parameters
        ----------
        alertclasses_update:
            alertclasses_update
        Returns
        -------
        AlertclassesUpdateReturns:
            alertclasses_update_returns
        """
        ...

class AlertclassesEntry(typing.TypedDict):
        id:'int'
        classes:'dict[str]'
        ...
class AlertclassesUpdate(typing.TypedDict):
        classes:'dict[str]'
        ...
class AlertclassesUpdateReturns(typing.TypedDict):
        id:'int'
        classes:'dict[str]'
        ...
