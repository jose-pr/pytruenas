import json
from pathlib import Path as _P
import re as _re
import keyword as _kw
import typing as _ty
from .._core import NamespaceInfo, Method, Parameter
from ..base import TrueNASClient
from .. import _utils

class NamespaceCodegen:
    def generate(
        self, namespace: NamespaceInfo, exportas: str, modname: str
    ) -> tuple[str, str] | str:
        ...


def _openapi_to_python_type(ty: str | list[str]):
    if isinstance(ty, list):
        return [_openapi_to_python_type(t) for t in ty]
    match ty:
        case 'null':
            ty = None
        case "boolean":
            ty = bool
        case "integer":
            ty = int
        case "string":
            ty = str
        case "array":
            ty = list
        case "object":
            ty = dict[str]
        case _:
            pass
    return ty


class Codegen:
    def __init__(self, nscodegen: NamespaceCodegen) -> None:
        self.nscodegen = nscodegen

    def resolve_parameter(self, param: Parameter):
        if not param:
            return {
                "type": None,
                "description": "",
                "title": "",
                "name": "",
            }
        else:
            param['name'] = param["name"].replace('-','_')
            if "type" in param:
                param["type"] = _openapi_to_python_type(param["type"])
            else:
                if 'anyOf' in param:
                    param['type'] = [ _openapi_to_python_type(t['type']) for t in param['anyOf'] ]
                pass
            default = param.get('default', _utils.MISSING)
            if default is not _utils.MISSING:
                match default:
                    case True:
                        ...
                    case False:
                        ...
                    case None:
                        ...
                    case _:
                        default = json.dumps(default)
                param['default'] = default
            
        return param

    def generate(self, client: TrueNASClient, root: _P | str):
        root = _P(root)
        root.mkdir(exist_ok=True)

        with (root / "__init__.py").open("w") as index:
            for ns in sorted(
                client.namespaces(), key=lambda ns: ns["config"]["namespace"]
            ):
                name = ns["config"]["namespace"]
                modname = ".".join(
                    [(f"{n}_" if _kw.iskeyword(n) else n) for n in name.split(".")]
                )
                exportas = (
                    modname[0].upper()
                    + _re.sub("\.[a-z]", lambda m: m.group(0)[1:].upper(), name)[1:]
                )
                ns_path = root / modname.replace(".", "/")
                ns_path.mkdir(exist_ok=True, parents=True)
                srv_ini = ns_path / "__init__.py"
                for m in ns["methods"].values():
                    for s in ["accepts", "returns"]:
                        m[s] = [self.resolve_parameter(p) for p in m[s]]
                code = self.nscodegen.generate(ns, exportas, modname)
                if isinstance(code, str):
                    code = [code]
                code, typings, *_ = [*code, None, None]
                srv_ini.write_text(code)
                if typings:
                    srv_ini.with_suffix(".pyi").write_text(typings)
                index.write(f"from .{modname} import {exportas}\n")
