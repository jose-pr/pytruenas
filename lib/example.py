#!/bin/python3
from pytruenas import TrueNASClient, Credentials

import os, sys
import logging

handler = logging.StreamHandler(sys.stderr)
logging.getLogger().addHandler(handler)


tn_host = os.environ.get("TN_HOST")
tn_creds = Credentials.from_env()
client = TrueNASClient(tn_host, tn_creds, sslverify=False)
client.logger.setLevel(logging.TRACE)

state = client.api.directoryservices.status()
print(state)


