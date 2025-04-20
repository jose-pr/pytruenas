#!/bin/python3
from pytruenas import TrueNASClient, Credentials

import os, sys
import logging
from pytruenas.utils import sql as sqlutils

handler = logging.StreamHandler(sys.stderr)
logging.getLogger().addHandler(handler)

tn_host = os.environ.get("TN_HOST")
tn_creds = Credentials.from_env()
client = TrueNASClient(tn_host, tn_creds, sslverify=False)
client.logger.setLevel(logging.TRACE)

pytruenaskey = client.api.keychaincredential._get(type='SSH_KEY_PAIR', name='pytruenas')
if not pytruenaskey:
    key = client.api.keychaincredential.generate_ssh_key_pair()
    pytruenaskey = client.api.keychaincredential._upsert('name', type='SSH_KEY_PAIR', name='pytruenas', attributes=key)
pubkey = pytruenaskey['attributes']['public_key'].strip()
root = client.api.user._get(username='root')
rootauthkeys = (root.get('sshpubkey') or '').splitlines()

if pubkey not in rootauthkeys:
    rootauthkeys.append(pubkey)
    client.api.user._upsert('username', username='root', sshpubkey='\n'.join(rootauthkeys))

client.shell.logintype = 'client_keys'
client.shell.credentials = pytruenaskey["attributes"]['private_key']

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

state = client.api.directoryservices.status()
users = client.api.user._query(username=sqlutils.RE("adm.*"))
admin = client.api.user._get(username="admin")
print(users)
print(admin)
