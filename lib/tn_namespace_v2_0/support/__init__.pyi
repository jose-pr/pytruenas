
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Support(
    Namespace
    ):
    _namespace:typing.Literal['support']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def attach_ticket(self, 
        attach_ticket:'AttachTicket',
    /) -> None: 
        """
        Method to attach a file to a existing ticket.

        Parameters
        ----------
        attach_ticket:
            attach_ticket
        Returns
        -------
        """
        ...
    @typing.overload
    def attach_ticket_max_size(self, 
    /) -> 'int': 
        """
        Returns maximum uploaded file size for `support.attach_ticket`

        Parameters
        ----------
        Returns
        -------
        int:
            attach_ticket_max_size
        """
        ...
    @typing.overload
    def config(self, 
    /) -> 'SupportEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        SupportEntry:
            support_entry
        """
        ...
    @typing.overload
    def fetch_categories(self, 
        token:'str',
    /) -> 'dict[str]': 
        """
        Fetch issue categories using access token `token`.
        Returns a dict with the category name as a key and id as value.

        Parameters
        ----------
        token:
            token
        Returns
        -------
        dict[str]:
            Example(s):
            ```
            {
                "API": "11008",
                "WebUI": "10004"
            }
            ```
        """
        ...
    @typing.overload
    def fields(self, 
    /) -> 'list[list[str]]': 
        """
        Returns list of pairs of field names and field titles for Proactive Support.

        Parameters
        ----------
        Returns
        -------
        list[list[str]]:
            support_fields
        """
        ...
    @typing.overload
    def is_available(self, 
    /) -> 'bool': 
        """
        Returns whether Proactive Support is available for this product type and current license.

        Parameters
        ----------
        Returns
        -------
        bool:
            proactive_support_is_available
        """
        ...
    @typing.overload
    def is_available_and_enabled(self, 
    /) -> 'bool': 
        """
        Returns whether Proactive Support is available and enabled.

        Parameters
        ----------
        Returns
        -------
        bool:
            proactive_support_is_available_and_enabled
        """
        ...
    @typing.overload
    def new_ticket(self, 
        new_ticket:'NewTicket',
    /) -> 'NewTicketResponse': 
        """
        Creates a new ticket for support.
        This is done using the support proxy API.
        For TrueNAS SCALE it will be created on JIRA and for TrueNAS SCALE Enterprise on Salesforce.
        
        For SCALE `criticality`, `environment`, `phone`, `name` and `email` attributes are not required.
        For SCALE Enterprise `token` and `type` attributes are not required.

        Parameters
        ----------
        new_ticket:
            new_ticket
        Returns
        -------
        NewTicketResponse:
            new_ticket_response
        """
        ...
    @typing.overload
    def update(self, 
        support_update:'SupportUpdate',
    /) -> 'SupportUpdateReturns': 
        """
        Update Proactive Support settings.

        Parameters
        ----------
        support_update:
            support_update
        Returns
        -------
        SupportUpdateReturns:
            support_update_returns
        """
        ...
    AttachTicket = typing.TypedDict('AttachTicket', {
            'ticket':'int',
            'filename':'str',
            'token':'str',
    })
    SupportEntry = typing.TypedDict('SupportEntry', {
            'enabled':'typing.Optional[bool]',
            'name':'str',
            'title':'str',
            'email':'str',
            'phone':'str',
            'secondary_name':'str',
            'secondary_title':'str',
            'secondary_email':'str',
            'secondary_phone':'str',
            'id':'int',
    })
    NewTicket = typing.TypedDict('NewTicket', {
            'title':'str',
            'body':'str',
            'category':'str',
            'attach_debug':'bool',
            'token':'str',
            'type':'Type',
            'criticality':'str',
            'environment':'str',
            'phone':'str',
            'name':'str',
            'email':'str',
            'cc':'list[str]',
    })
    class Type(str,Enum):
        BUG = 'BUG'
        FEATURE = 'FEATURE'
        ...
    NewTicketResponse = typing.TypedDict('NewTicketResponse', {
            'ticket':'typing.Optional[int]',
            'url':'typing.Optional[str]',
            'has_debug':'bool',
    })
    SupportUpdate = typing.TypedDict('SupportUpdate', {
            'enabled':'typing.Optional[bool]',
            'name':'str',
            'title':'str',
            'email':'str',
            'phone':'str',
            'secondary_name':'str',
            'secondary_title':'str',
            'secondary_email':'str',
            'secondary_phone':'str',
    })
    SupportUpdateReturns = typing.TypedDict('SupportUpdateReturns', {
            'enabled':'typing.Optional[bool]',
            'name':'str',
            'title':'str',
            'email':'str',
            'phone':'str',
            'secondary_name':'str',
            'secondary_title':'str',
            'secondary_email':'str',
            'secondary_phone':'str',
            'id':'int',
    })
