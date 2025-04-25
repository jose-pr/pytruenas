#!/bin/python3
from pytruenas import TrueNASClient, Credentials
import os, sys
import logging
from pytruenas.utils import query
import asyncssh as _ssh

handler = logging.StreamHandler(sys.stderr)
logging.getLogger().addHandler(handler)

tn_host = os.environ.get("TN_HOST")
tn_creds = Credentials.from_env()
client = TrueNASClient(tn_host, tn_creds, sslverify=False)
client.logger.setLevel(logging.TRACE)

users = client.api.user._query(username=query.RE("adm.*"))
admin = client.api.user._get(username="admin")
print(len(users))
print(admin["username"])

data = client.api.pool.dataset._get("data")
print(data["name"])

ssh_service = client.api.service._update(("service",), service="ssh", enable=True)
print(ssh_service)


netconfig = client.api.network.configuration.config()
netconfig = client.api.network.configuration._update(hostname=netconfig["hostname"])
hostname: str = netconfig["hostname"]
print(hostname)

keypair_name = hostname.upper()
keypair = client.api.keychaincredential._get(type="SSH_KEY_PAIR", name=keypair_name)
if not keypair:
    private_key = client.api.keychaincredential.generate_ssh_key_pair()["private_key"]
else:
    private_key = keypair["attributes"]["private_key"]

pubkey = _ssh.import_private_key(private_key).export_public_key().decode().strip()

keypair = client.api.keychaincredential._upsert(
    ("name", "!type"),
    type="SSH_KEY_PAIR",
    name=keypair_name,
    attributes={"private_key": private_key, "public_key": pubkey},
)

try:
    client.api.keychaincredential._create(
        ("name", "type"),
        type="SSH_KEY_PAIR",
        name=keypair_name,
        attributes={"private_key": private_key, "public_key": pubkey},
    )
except FileExistsError as e:
    print("SSH Key Pair exists", e.args[0])