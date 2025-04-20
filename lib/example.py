#!/bin/python3
from pytruenas import TrueNASClient, Credentials

import os, sys
import logging
from pytruenas.utils import sql as sqlutils

handler = logging.StreamHandler(sys.stderr)
logging.getLogger().addHandler(handler)


query = sqlutils.filter_from_kwargs(test=1, bob="test", bob2=sqlutils.EQ("equalto"))
print(query)

tn_host = os.environ.get("TN_HOST")
tn_creds = Credentials.from_env()
client = TrueNASClient(tn_host, tn_creds, sslverify=False)
client.logger.setLevel(logging.TRACE)

result = TrueNASClient().run(
    ("echo", "'\"text\"'"),
    ("ls", "-l", "/mnt"),
    "echo test",
    capture_output=True,
    encoding="utf8",
)
print(result.stdout)

state = client.api.directoryservices.status()
users = client.api.user._query(username=sqlutils.RE("adm.*"))
admin = client.api.user._get(username="admin")
print(users)
print(admin)
