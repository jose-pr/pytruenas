
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Alert(Namespace):
    _namespace:_ty.Literal['alert']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def dismiss(self, 
        uuid:'str',
    /) -> None: 
        """
        Dismiss `id` alert.

        Parameters
        ----------
        uuid:
            uuid
        Returns
        -------
        """
        ...
    @_ty.overload
    def list(self, 
    /) -> 'list': 
        """
        List all types of alerts including active/dismissed currently in the system.

        Parameters
        ----------
        Returns
        -------
        list:
            alerts
        """
        ...
    @_ty.overload
    def list_categories(self, 
    /) -> 'list': 
        """
        List all types of alerts which the system can issue.

        Parameters
        ----------
        Returns
        -------
        list:
            categories
        """
        ...
    @_ty.overload
    def list_policies(self, 
    /) -> 'list': 
        """
        List all alert policies which indicate the frequency of the alerts.

        Parameters
        ----------
        Returns
        -------
        list:
            alert_policies
        """
        ...
    @_ty.overload
    def restore(self, 
        uuid:'str',
    /) -> None: 
        """
        Restore `id` alert which had been dismissed.

        Parameters
        ----------
        uuid:
            uuid
        Returns
        -------
        """
        ...
