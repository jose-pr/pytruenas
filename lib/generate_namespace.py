#!/bin/python3
from pathlib import Path

from pytruenas import TrueNASClient, Namespace, namespace
from pytruenas.codegen import Codegen, mako, NamespaceSignature
from pytruenas import mixins
import os
import shutil

# tn_host = os.environ['TN_HOST']
# tn_apikey = os.environ['TN_APIKEY']
# client = TrueNASClient(tn_host, tn_apikey)
client = TrueNASClient()

namespaces_path = Path("./lib/tn_namespace_v2_0").resolve()
shutil.rmtree(namespaces_path, ignore_errors=True)


codegen = Codegen(mako.NamespaceCodegen())
codegen.generate(client, namespaces_path)


def mixinsfn(ns: NamespaceSignature):
    match ns._raw["type"]:
        case "crud":
            return Namespace, [mixins.TableExtMixin]
        case "config":
            return Namespace, [mixins.ConfigMixin]
        case _:
            return None, None


codegen.generate(
    client, namespaces_path.with_name(namespaces_path.name + "_mixins"), mixinsfn
)

pass
