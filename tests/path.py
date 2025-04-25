#!/bin/python3
from pytruenas import TrueNASClient, Credentials, fs
import os, sys
import logging

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


handler = logging.StreamHandler(sys.stderr)
logging.getLogger().addHandler(handler)

tn_host = os.environ.get("TN_HOST")
tn_creds = Credentials.from_env()
client = TrueNASClient(tn_host, tn_creds, sslverify=False)
client.logger.setLevel(logging.DEBUG)

fs.local.FORCE_LOCAL = True
datapool = client.path("/mnt/data", backend="local")
testfiles = datapool / "testfiles"
print(repr(testfiles))

testfiles.mkdir(exist_ok=True)

client.install_sshcreds()

for backend in fs.BACKENDS:
    testfile = testfiles.with_backend(backend) / backend
    print(repr(testfile))

    testfile.mkdir(parents=False, exist_ok=True)
    try:
        testfile.rmdir()
    except NotImplementedError as e:
        print(f"Mkdir not supported for {backend}")

    testfile = testfile.with_suffix('.txt')
    testfile.write_text(f"Test of backend {backend}")
    print(testfile.read_text())
    print(testfile.stat())
    try:
        testfile.unlink()
    except NotImplementedError as e:
        print(f"unlink not supported for {backend}")


