
from pytruenas.base import Namespace

import typing
from enum import Enum

class Support(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'support')

    AttachTicket = typing.TypedDict('AttachTicket', {
            'ticket':'int',
            'filename':'str',
            'token':'str',
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
    NewTicketResponse = typing.TypedDict('NewTicketResponse', {
            'ticket':'typing.Optional[int]',
            'url':'typing.Optional[str]',
            'has_debug':'bool',
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
    class Type(str,Enum):
        BUG = 'BUG'
        FEATURE = 'FEATURE'
        ...
