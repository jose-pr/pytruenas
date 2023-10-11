
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Alert(
    Namespace
    ):
    _namespace:typing.Literal['alert']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def dismiss(self, 
        _uuid:'str',
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
    @typing.overload
    def list(self, 
    /) -> 'list[Alert]': 
        """
        List all types of alerts including active/dismissed currently in the system.

        Parameters
        ----------
        Returns
        -------
        list[Alert]:
            alerts
        """
        ...
    @typing.overload
    def list_categories(self, 
    /) -> 'list[Category]': 
        """
        List all types of alerts which the system can issue.

        Parameters
        ----------
        Returns
        -------
        list[Category]:
            categories
        """
        ...
    @typing.overload
    def list_policies(self, 
    /) -> 'list[Policy]': 
        """
        List all alert policies which indicate the frequency of the alerts.

        Parameters
        ----------
        Returns
        -------
        list[Policy]:
            alert_policies
        """
        ...
    @typing.overload
    def restore(self, 
        _uuid:'str',
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
    Alert = typing.TypedDict('Alert', {
            'uuid':'str',
            'source':'str',
            'klass':'str',
            'args':'typing.Union[str, int, bool, dict[str], list]',
            'node':'str',
            'key':'str',
            'datetime':'str',
            'last_occurrence':'str',
            'dismissed':'bool',
            'mail':'typing.Union[str, int, bool, dict[str], list]',
            'text':'str',
            'id':'str',
            'level':'str',
            'formatted':'typing.Optional[str]',
            'one_shot':'bool',
    })
    Category = typing.TypedDict('Category', {
            'id':'str',
            'title':'str',
            'classes':'list[CategoryClass]',
    })
    CategoryClass = typing.TypedDict('CategoryClass', {
            'id':'str',
            'title':'str',
            'level':'str',
            'proactive_support':'bool',
    })
    class Policy(str,Enum):
        IMMEDIATELY = 'IMMEDIATELY'
        HOURLY = 'HOURLY'
        DAILY = 'DAILY'
        NEVER = 'NEVER'
        ...
