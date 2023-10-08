import json
from enum import Enum as _Enum
from pathlib import Path as _P
import re as _re
import keyword as _kw
import typing as _ty
from ..base import TrueNASClient
from .. import _utils, _core


class OpenApiType(_ty.NamedTuple):
    raw: _core.Parameter|str

    def python(self) -> str:
        ty = self.raw["type"] if isinstance(self.raw, dict) else self.raw
        match ty:
            case "null":
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
                raise ValueError(ty)
        if "<" in str(ty):
            ty = ty.__name__
        return str(ty)


class Paramater(_ty.NamedTuple):
    type: list[OpenApiType]
    description: str
    default: "_ty.Any"
    required: bool

    @classmethod
    def from_param(cls, param: "_core.Parameter"):
        param = param or {}
        type = []
        desc = param.get("description", param.get('title', ''))
        required = param.get("required", True)
        _found = False
        for k in ['type', 'anyOf']:
            if k in param:
                _type = param[k]
                if not isinstance(_type, list):
                    _type = [_type]
                type = [OpenApiType(t) for t in _type]
                _found = True
        if not _found:
            pass
        default = param.get("default", _utils.MISSING)
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
        return cls(type, desc, default, required)


class MethodSignature(_ty.NamedTuple):
    description: str
    arguments: _ty.OrderedDict[str, Paramater]
    returns: list[Paramater]


class NamespaceSignature:
    _raw: _core.NamespaceInfo
    methods: dict[str, list[MethodSignature]]

    def __init__(self, raw: _core.NamespaceInfo) -> None:
        self._raw = raw
        self.methods = {}
        for name, method in self._raw["methods"].items():
            signatures = []
            descr = method["description"]
            returns = []
            args = _ty.OrderedDict()
            for p in method["accepts"]:
                pname = p["name"].replace("-", "_")
                args[pname] = Paramater.from_param(p)
            for p in method["returns"]:
                returns.append(Paramater.from_param(p))
            signatures.append(MethodSignature(descr, args, returns))
            self.methods[name] = signatures

    @property
    def description(self):
        return self._raw["config"]["cli_description"]

    @property
    def dotname(self):
        return self._raw["config"]["namespace"]

    @property
    def module(self):
        return ".".join(
            [(f"{n}_" if _kw.iskeyword(n) else n) for n in self.dotname.split(".")]
        )

    @property
    def modpath(self):
        return _P(self.module.replace(".", "/"))

    @property
    def classname(self):
        return (
            self.module[0].upper()
            + _re.sub("\.[a-z]", lambda m: m.group(0)[1:].upper(), self.module)[1:]
        )


class NamespaceCodegen:
    def generate(
        self,
        namespace: NamespaceSignature,
    ) -> tuple[str, str] | str:
        ...


_INIT = "__init__.py"


class Codegen:
    def __init__(self, nscodegen: NamespaceCodegen) -> None:
        self.nscodegen = nscodegen

    def generate(self, client: TrueNASClient, root: _P | str):
        root = _P(root)
        root.mkdir(exist_ok=True)

        with (root / _INIT).open("w") as index:
            for ns in sorted(
                client.namespaces(), key=lambda ns: ns["config"]["namespace"]
            ):
                ns = NamespaceSignature(ns)
                code = self.nscodegen.generate(ns)
                if isinstance(code, str):
                    code = [code]
                code, typings, *_ = [*code, None, None]
                ns_path = root / ns.modpath / _INIT
                ns_path.parent.mkdir(exist_ok=True, parents=True)
                ns_path.write_text(code)
                if typings:
                    ns_path.with_suffix(".pyi").write_text(typings)
                index.write(f"from .{ns.module} import {ns.modpath}\n")
