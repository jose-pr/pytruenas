#!/bin/python3
# type: ignore

from pytruenas import TrueNASClient, Credentials, fs
import pathlib
import os, sys
import logging
import typing

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


handler = logging.StreamHandler(sys.stderr)
logging.getLogger().addHandler(handler)

tn_host = os.environ.get("TN_HOST")
tn_creds = Credentials.from_env()
client = TrueNASClient(tn_host, tn_creds, sslverify=False)
client.logger.setLevel(logging.DEBUG)

print(typing.get_args(fs._FTYPE))

fs.local.FORCE_LOCAL = True
datapool = client.path("/mnt/data", backend="local")
testfiles = datapool / "testfiles"
testfiles.mkdir(exist_ok=True)

client.install_sshcreds()
print('Data Pool Is Mount', datapool.with_backend('sftp').is_mount())
print('Directory Is Mount', testfiles.with_backend('sftp').is_mount())

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
        linkto = testfile.with_suffix('.link')
        linkto.with_backend('local').unlink(True)
        linkto.symlink_to(testfile)
        print(linkto.is_symlink(), linkto.read_text())
    except NotImplementedError as e:
        print(f"Symlink not supported for {backend}")

    try:
        testfile.unlink()
    except NotImplementedError as e:
        print(f"unlink not supported for {backend}")

datapool = datapool.with_backend('sftp')
for file in datapool.iterdir():
    print(file, file.is_symlink(), file.is_dir(), file.is_file())

print((datapool / 'unknown').is_symlink())
