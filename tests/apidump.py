#!/bin/python3
from pytruenas import TrueNASClient, Credentials

import os, sys
import logging
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
    client.install_sshcreds()
    apidump = client.dump_api()

stubspath = Path('lib/truenasapi_typings')
from pytruenas.codegen import Codegen
codegen = Codegen()
for version in apidump['versions']:
    print(f"Supports api {version['version']}")
    name = version["version"].replace('.', '_')
    codegen.generate(version, stubspath / name)