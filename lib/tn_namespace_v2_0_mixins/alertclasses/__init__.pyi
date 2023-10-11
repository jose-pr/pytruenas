
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin
from enum import Enum
import typing
class Alertclasses(
    ConfigMixin,
    Namespace
    ):
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
        alertclasses_update:'AlertclassesUpdate',
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
    AlertclassesEntry = typing.TypedDict('AlertclassesEntry', {
            'id':'int',
            'classes':'dict[str]',
    })
    AlertclassesUpdate = typing.TypedDict('AlertclassesUpdate', {
            'classes':'dict[str]',
    })
    AlertclassesUpdateReturns = typing.TypedDict('AlertclassesUpdateReturns', {
            'id':'int',
            'classes':'dict[str]',
    })
