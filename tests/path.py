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


datapool = client.path('/mnt/data', methods='local')
datapool2 = client.path('/mnt/data', methods='auto')
print(repr(datapool), repr(datapool2))
testfile = client.path('/mnt/data/testfile', methods = 'api')


testfile.write_bytes(b'test data 1234')
print(testfile.read_text())
print(testfile.stat())
print(TrueNASClient().path(testfile, methods='local').stat())
with testfile.open('wb') as fh:
    fh.write(b'test2')
with testfile.open('rb') as fh:
    print(fh.read())
with testfile.open('w') as fh:
    fh.write('test3')
with testfile.open('r') as fh:
    print(fh.read())
exit()
client.install_sshcreds()


print(datapool.parent)
print(datapool.stat(_force_local=True))
print(datapool.exists(_force_local=True))
print((datapool / 'doesnt exists').exists(_force_local=False))