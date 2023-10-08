
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Support(Namespace):
    _namespace:_ty.Literal['support']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def attach_ticket(self, 
        attach_ticket:'dict[str]'={},
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
    @_ty.overload
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
    @_ty.overload
    def config(self, 
    /) -> 'dict[str]': 
        """
        

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            support_entry
        """
        ...
    @_ty.overload
    def fetch_categories(self, 
        token:'str'="",
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
    @_ty.overload
    def fields(self, 
    /) -> 'list': 
        """
        Returns list of pairs of field names and field titles for Proactive Support.

        Parameters
        ----------
        Returns
        -------
        list:
            support_fields
        """
        ...
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
    def new_ticket(self, 
        new_ticket:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            new_ticket_response
        """
        ...
    @_ty.overload
    def update(self, 
        support_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update Proactive Support settings.

        Parameters
        ----------
        support_update:
            support_update
        Returns
        -------
        dict[str]:
            support_update_returns
        """
        ...
