from pathlib import Path
 
from pytruenas import TrueNASClient, Namespace, namespace
from pytruenas.codegen import Codegen, mako
import os
import shutil

tn_host = os.environ['TN_HOST']
tn_apikey = os.environ['TN_APIKEY']
#client = TrueNASClient(tn_host, tn_apikey)
client = TrueNASClient()

namespaces_path = Path('./lib/_namespaces').resolve()
shutil.rmtree(namespaces_path, ignore_errors=True)


codegen = Codegen(mako.NamespaceCodegen())
codegen.generate(client, namespaces_path)

pass