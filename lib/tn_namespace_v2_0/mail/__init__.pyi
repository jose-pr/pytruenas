
from pytruenas import Namespace, TrueNASClient
import typing
class Mail(Namespace):
    _namespace:typing.Literal['mail']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def config(self, 
    /) -> 'MailEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        MailEntry:
            mail_entry
        """
        ...
    @typing.overload
    def send(self, 
        mail_message:'MailMessage'={},
        mail_update:'MailUpdate'={},
    /) -> 'bool': 
        """
        Sends mail using configured mail settings.
        
        `text` will be formatted to HTML using Markdown and rendered using default E-Mail template.
        You can put your own HTML using `html`. If `html` is null, no HTML MIME part will be added to E-Mail.
        
        If `attachments` is true, a list compromised of the following dict is required
        via HTTP upload:
          - headers(list)
            - name(str)
            - value(str)
            - params(dict)
          - content (str)
        
        [
         {
          "headers": [
           {
            "name": "Content-Transfer-Encoding",
            "value": "base64"
           },
           {
            "name": "Content-Type",
            "value": "application/octet-stream",
            "params": {
             "name": "test.txt"
            }
           }
          ],
          "content": "dGVzdAo="
         }
        ]

        Parameters
        ----------
        mail_message:
            mail_message
        mail_update:
            mail_update
        Returns
        -------
        bool:
            successfully_sent
        """
        ...
    @typing.overload
    def update(self, 
        mail_update:'MailUpdate_'={},
    /) -> 'MailUpdateReturns': 
        """
        Update Mail Service Configuration.
        
        `fromemail` is used as a sending address which the mail server will use for sending emails.
        
        `outgoingserver` is the hostname or IP address of SMTP server used for sending an email.
        
        `security` is type of encryption desired.
        
        `smtp` is a boolean value which when set indicates that SMTP authentication has been enabled and `user`/`pass`
        are required attributes now.

        Parameters
        ----------
        mail_update:
            mail_update
        Returns
        -------
        MailUpdateReturns:
            mail_update_returns
        """
        ...

class MailEntry(typing.TypedDict):
        fromemail:'str'
        fromname:'str'
        outgoingserver:'str'
        port:'int'
        security:'str'
        smtp:'bool'
        user:'typing.Optional[str]'
        pass:'typing.Optional[str]'
        oauth:'Oauth'
        id:'int'
        ...
class Oauth(typing.TypedDict):
        client_id:'str'
        client_secret:'str'
        refresh_token:'str'
        ...
class MailMessage(typing.TypedDict):
        subject:'str'
        text:'str'
        html:'typing.Optional[str]'
        to:'list[str]'
        cc:'list[str]'
        interval:'typing.Optional[int]'
        channel:'typing.Optional[str]'
        timeout:'int'
        attachments:'bool'
        queue:'bool'
        extra_headers:'dict[str]'
        ...
class MailUpdate(typing.TypedDict):
        fromemail:'str'
        fromname:'str'
        outgoingserver:'str'
        port:'int'
        security:'str'
        smtp:'bool'
        user:'typing.Optional[str]'
        pass:'typing.Optional[str]'
        oauth:'Oauth'
        ...
class Oauth_(typing.TypedDict):
        client_id:'str'
        client_secret:'str'
        refresh_token:'str'
        ...
class MailUpdate_(typing.TypedDict):
        fromemail:'str'
        fromname:'str'
        outgoingserver:'str'
        port:'int'
        security:'str'
        smtp:'bool'
        user:'typing.Optional[str]'
        pass:'typing.Optional[str]'
        oauth:'Oauth'
        ...
class MailUpdateReturns(typing.TypedDict):
        fromemail:'str'
        fromname:'str'
        outgoingserver:'str'
        port:'int'
        security:'str'
        smtp:'bool'
        user:'typing.Optional[str]'
        pass:'typing.Optional[str]'
        oauth:'Oauth'
        id:'int'
        ...
