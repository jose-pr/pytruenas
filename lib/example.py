#!/bin/python3
from pytruenas import TrueNASClient, Credentials
from pytruenas.mixins import UpdateReturn

import os

from pytruenas.mixins import TableExtMixin


tn_host = os.environ.get("TN_HOST")
tn_creds = Credentials.from_env()
client = TrueNASClient(tn_host, tn_creds, sslverify=False)

from tn_namespace_v2_0 import Cronjob as _Cronjob, Auth
from tn_namespace_v2_0_mixins import SystemAdvanced, PoolDataset
#
# Extend automatic generated namespace with some methods for Map/list
#
class Cronjob(TableExtMixin[_Cronjob.CronJobEntry], _Cronjob):
    ...


api = client.api()
sysadv = SystemAdvanced(client)
config = sysadv.config()
choices = PoolDataset(client).encryption_algorithm_choices()
cronjobs = Cronjob(client)
count = len(cronjobs)
_cronjobs = cronjobs.query()
_first = _cronjobs[0] if cronjobs else None
firstid = _first["id"] if cronjobs else None
assert cronjobs.get(firstid, None) == _first
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
