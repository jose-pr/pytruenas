#!/bin/python3
from pytruenas import TrueNASClient, Credentials
import typing
if typing.TYPE_CHECKING:
    from truenasapi_typings.current import Current
import os, sys
import logging
from pytruenas.utils import sql as sqlutils
import json
from pathlib import Path

handler = logging.StreamHandler(sys.stderr)
logging.getLogger().addHandler(handler)

tn_host = os.environ.get("TN_HOST")
tn_creds = Credentials.from_env()
client = TrueNASClient['Current'](tn_host, tn_creds, sslverify=False)
client.logger.setLevel(logging.DEBUG)

client.load_sshcreds()

result = TrueNASClient().run(
    ("echo", "'\"text\"'"),
    ("ls", "-l", "/mnt"),
    "echo test",
    capture_output=True,
    encoding="utf8",
)
print(result.stdout)

result = client.run(
    ("echo", "'\"text\"'"),
    ("ls", "-l", "/mnt"),
    "echo test",
    capture_output=True,
    encoding="utf8",
)
print(result.stdout)

state = client.api.sharing.smb.getacl()
users = client.api.user._query(username=sqlutils.RE("adm.*"))
admin = client.api.user._get(username="admin")
print(users)
print(admin)
cache = Path('_api.json')
if cache.exists():
    apidump = json.loads(cache.read_text())
else:
    apidump = client.dump_api()
for version in apidump["versions"]:
    print(f"Supports api {version['version']}")
    for method in version["methods"]:
        name = method["name"]
        print(f"First method: {name}")
        roles = method["roles"]
        schema = method["schemas"]
        callparameters = schema["properties"]["Call parameters"]
        returnvalue = schema["properties"]["Return value"]
        print(f"Call Parameters: {callparameters}")
        print(f"Return Value: {returnvalue}")
