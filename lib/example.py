#!/bin/bash
from pytruenas import TrueNASClient, Creds, AuthMethod, Config, UpdateReturn
from pytruenas.auth import Auth, Session
from pytruenas.system import SystemGeneral

client = TrueNASClient()
sysgeneral = SystemGeneral(client)
config = sysgeneral.config()
port = config['ui_port']
timezones = sysgeneral.timezone_choices()
diff, config = sysgeneral.update({"ui_port": 81},  _return=UpdateReturn.Both, ui_port=80, ui_httpsport=443)
print(f"Changes: {diff}")
if sysgeneral.update(_return=UpdateReturn.Diff, ui_port=port):
    print("Settings changed back")
auth = Auth(client)
whoami = auth.me()
sessions = auth.sessions()
pass
