#!/bin/python3
from pytruenas import TrueNASClient, Creds, AuthMethod
from pytruenas.mixins import UpdateReturn

import os
from typing import TypedDict

from pytruenas.mixins import TableExtMixin
from tn_namespace_v2_0 import Cronjob as _Cronjob, Auth
from tn_namespace_v2_0_exts import SystemGeneral


class CronjobEntry(TypedDict):
    id: int
    ...


#
# Extend automatic generated namespace with some methods for Map/list
#
class Cronjob(TableExtMixin[_Cronjob.CronJobEntry], _Cronjob):
    ...


tn_host = os.environ["TN_HOST"]
tn_apikey = os.environ["TN_APIKEY"]
client = TrueNASClient(tn_host, tn_apikey, sslverify=False)
sysgeneral = SystemGeneral(client)
config = sysgeneral.config()
port = config["ui_port"]
timezones = sysgeneral.timezone_choices()
cronjobs = Cronjob(client)
count = len(cronjobs)
_cronjobs = cronjobs.query()
_first = _cronjobs[0] if cronjobs else None
firstid = _first["id"] if cronjobs else None
assert cronjobs.get(firstid, None) == _first
#
# By default returns the new config
#
config = sysgeneral.update({"ui_port": 80})
#
# Get the changes and the full config
#
diff, config = sysgeneral.update(
    {"ui_port": 81}, _return=UpdateReturn.Both, ui_port=80, ui_httpsport=443
)
print(f"Changes: {diff}")
#
# Only do an action if config changed
#
if sysgeneral.update(_return=UpdateReturn.Diff, ui_port=port):
    print("Settings changed back")
auth = Auth(client)
try:
    whoami = auth.me()
except:
    # Will fail when using api keys
    ...
sessions: list[Auth.Session] = auth.sessions()
token = auth.generate_token(10)

print(token)
pass
