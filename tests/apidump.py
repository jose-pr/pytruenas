#!/bin/python3
from pytruenas import TrueNASClient, Credentials

import os, sys
import logging
from pytruenas.utils import sql as sqlutils
import json
from pathlib import Path

handler = logging.StreamHandler(sys.stderr)
logging.getLogger().addHandler(handler)

tn_host = os.environ.get("TN_HOST")
tn_creds = Credentials.from_env()
client = TrueNASClient(tn_host, tn_creds, sslverify=False)
client.logger.setLevel(logging.DEBUG)

cache = Path('_api.json')
if cache.exists():
    apidump = json.loads(cache.read_text())
else:
    client.load_sshcreds()
    apidump = client.dump_api()

stubspath = Path('lib/truenasapi_typings')

for version in apidump["versions"]:
    print(f"Supports api {version['version']}")

from pytruenas.models import apidump as api

def typings_for_apiversion(version:api.Version):
    for method in version["methods"]:
        name = method["name"]
        print(f"{name}")
        roles = method["roles"]
        schema = method["schemas"]
        callparameters = schema["properties"]["Call parameters"]
        returnvalue = schema["properties"]["Return value"]
        break
        #print(f"Call Parameters: {callparameters}")
        #print(f"Return Value: {returnvalue}")
from pytruenas.codegen import Codegen
version = apidump["versions"][0]
codegen = Codegen()
name = version["version"].replace('.', '_')
codegen.generate(version, stubspath / name)