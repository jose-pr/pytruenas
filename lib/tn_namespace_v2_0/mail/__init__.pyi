
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Mail(Namespace):
    _namespace:_ty.Literal['mail']
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
            mail_entry
        """
        ...
    @_ty.overload
    def send(self, 
        mail_message:'dict[str]'={},
        mail_update:'dict[str]'={},
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
    @_ty.overload
    def update(self, 
        mail_update:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            mail_update_returns
        """
        ...
