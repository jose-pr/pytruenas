#!/bin/python3
from pytruenas import TrueNASClient, Creds, AuthMethod, Config, UpdateReturn
from pytruenas.namespace import *

client = TrueNASClient()
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
pass
