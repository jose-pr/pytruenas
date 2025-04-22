#!/bin/python3
from pytruenas import TrueNASClient, Credentials
import os, sys
import logging

handler = logging.StreamHandler(sys.stderr)
logging.getLogger().addHandler(handler)

tn_host = os.environ.get("TN_HOST")
tn_creds = Credentials.from_env()
client = TrueNASClient(tn_host, tn_creds, sslverify=False)
client.logger.setLevel(logging.DEBUG)

client.install_sshcreds()

datapool = client.path('/mnt/data', methods='local')

print(datapool)

print(datapool.parent)
print(datapool.stat(_force_local=True))
print(datapool.exists(_force_local=True))
print((datapool / 'doesnt exists').exists(_force_local=False))