#!/bin/python3
from pytruenas import TrueNASClient, Credentials
import typing
if typing.TYPE_CHECKING:
    from truenasapi_typings.current import Current
import os, sys
import logging
from pytruenas.utils import query
import json

from pytruenas.path import Path 

handler = logging.StreamHandler(sys.stderr)
logging.getLogger().addHandler(handler)

tn_host = os.environ.get("TN_HOST")
tn_creds = Credentials.from_env()
client = TrueNASClient['Current'](tn_host, tn_creds, sslverify=False)
client.logger.setLevel(logging.DEBUG)

client.install_sshcreds()

datapool = client.path('/mnt/data', methods='sftp')

print(datapool)

print(datapool.parent)

print(datapool.exists())
print(datapool.exists())
print(datapool.exists())