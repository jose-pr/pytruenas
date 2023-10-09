
from pytruenas import Namespace
import typing
class Mail(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'mail')

    Oauth = typing.TypedDict('Oauth', {
            'client_id':'str',
            'client_secret':'str',
            'refresh_token':'str',
    })
    MailEntry = typing.TypedDict('MailEntry', {
            'fromemail':'str',
            'fromname':'str',
            'outgoingserver':'str',
            'port':'int',
            'security':'str',
            'smtp':'bool',
            'user':'typing.Optional[str]',
            'pass':'typing.Optional[str]',
            'oauth':'Oauth',
            'id':'int',
    })
    MailMessage = typing.TypedDict('MailMessage', {
            'subject':'str',
            'text':'str',
            'html':'typing.Optional[str]',
            'to':'list[str]',
            'cc':'list[str]',
            'interval':'typing.Optional[int]',
            'channel':'typing.Optional[str]',
            'timeout':'int',
            'attachments':'bool',
            'queue':'bool',
            'extra_headers':'dict[str]',
    })
    Oauth_ = typing.TypedDict('Oauth_', {
            'client_id':'str',
            'client_secret':'str',
            'refresh_token':'str',
    })
    MailUpdate = typing.TypedDict('MailUpdate', {
            'fromemail':'str',
            'fromname':'str',
            'outgoingserver':'str',
            'port':'int',
            'security':'str',
            'smtp':'bool',
            'user':'typing.Optional[str]',
            'pass':'typing.Optional[str]',
            'oauth':'Oauth_',
    })
    MailUpdate_ = typing.TypedDict('MailUpdate_', {
            'fromemail':'str',
            'fromname':'str',
            'outgoingserver':'str',
            'port':'int',
            'security':'str',
            'smtp':'bool',
            'user':'typing.Optional[str]',
            'pass':'typing.Optional[str]',
            'oauth':'Oauth_',
    })
    MailUpdateReturns = typing.TypedDict('MailUpdateReturns', {
            'fromemail':'str',
            'fromname':'str',
            'outgoingserver':'str',
            'port':'int',
            'security':'str',
            'smtp':'bool',
            'user':'typing.Optional[str]',
            'pass':'typing.Optional[str]',
            'oauth':'Oauth',
            'id':'int',
    })
