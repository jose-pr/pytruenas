#!/bin/python3
from pytruenas import TrueNASClient, Creds, AuthMethod
from pytruenas.exts import UpdateReturn
from pytruenas.namespace.tns23 import *

from tn_namespaces import AcmeDnsAuthenticator

import os

tn_host = os.environ['TN_HOST']
tn_apikey = os.environ['TN_APIKEY']
client = TrueNASClient(tn_host, tn_apikey)
test= AcmeDnsAuthenticator(client)
sysgeneral = SystemGeneral(client)
config = sysgeneral.config()
port = config['ui_port']
timezones = sysgeneral.timezone_choices()
cronjobs = Cronjob(client)
count = cronjobs.get(1)
diff, config = sysgeneral.update({"ui_port": 81},  _return=UpdateReturn.Both, ui_port=80, ui_httpsport=443)
print(f"Changes: {diff}")
if sysgeneral.update(_return=UpdateReturn.Diff, ui_port=port):
    print("Settings changed back")
auth = Auth(client)
whoami = auth.me()
sessions = auth.sessions()

token = auth.generate_token()

print(token)
pass
