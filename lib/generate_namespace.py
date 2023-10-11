#!/bin/python3
from pathlib import Path

from pytruenas import TrueNASClient, Credentials
from pytruenas.codegen import Codegen, mako, PythonNamespaceSignature
from pytruenas import mixins
import shutil

import os
tn_host = os.environ.get("TN_HOST")
tn_creds = Credentials.from_env()
client = TrueNASClient(tn_host, tn_creds, sslverify=False)

namespaces_path = Path("./lib/tn_namespace_v2_0").resolve()
shutil.rmtree(namespaces_path, ignore_errors=True)


codegen = Codegen(mako.NamespaceCodegen())
codegen.generate(client, namespaces_path)


def mixinsfn(ns: PythonNamespaceSignature):
    match ns.type:
        case "crud":
            ns.mixins = [mixins.TableExtMixin]
        case "config":
            ns.mixins = [mixins.ConfigMixin]
        case "service":
            ...
        case _:
            pass
            ...

codegen.generate(
    client, namespaces_path.with_name(namespaces_path.name + "_mixins"), mixinsfn
)

pass
