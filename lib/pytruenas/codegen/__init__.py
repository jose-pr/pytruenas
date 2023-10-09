import json
from enum import Enum as _Enum
from pathlib import Path as _P
import re as _re
import keyword as _kw
import typing as _ty
from ..base import TrueNASClient
from .. import _utils, _core


class Object(_ty.NamedTuple):
    properties: _ty.OrderedDict[str, "OpenApiType"]


class OpenApiType:
    _raw: _core.Parameter
    _obj: str | None

    def __init__(self, raw: _core.Parameter | str, objects: dict[str, Object]):
        raw: _core.Parameter = raw if isinstance(raw, dict) else {"type": raw}
        self._raw = raw

        typescheck = ["anyOf", "oneOf", "items"]
        if "type" in raw and isinstance(raw["type"], str):
            pass
        else:
            typescheck.append("type")

        for k in typescheck:
            if k in raw:
                _type = raw[k]
                types = []
                if not isinstance(_type, list):
                    _type = [_type]
                for t in _type:
                    if isinstance(t, str):
                        t = {**raw, "type": t}
                    if not isinstance(t, OpenApiType):
                        t = OpenApiType(t, objects)
                    types.append(t)
                raw[k] = types
        obj = Object(_ty.OrderedDict())
        for name, prop in raw.get("properties", {}).items():
            obj.properties[name] = OpenApiType(prop, objects)

        if not obj.properties:
            self._obj = None
        else:
            name: str = self._raw.get("title", "Object")
            name = _utils.classname(name).rstrip("_")
            while name in objects and objects[name] != obj:
                name += "_"
            objects[name] = obj
            self._obj = name

    @property
    def type(self) -> "list[OpenApiType]|_core.Parameter":
        for k in ["type", "anyOf", "oneOf"]:
            if k in self._raw:
                ty = self._raw[k]
                if isinstance(ty, str):
                    return self._raw
                else:
                    return ty

    def python(self) -> 'type | Object':
        ty = self._python()
        if "<" in str(ty):
            ty = ty.__name__
        return str(ty).replace("'", "")

    def _python(self) -> str:
        types = self.type
        if isinstance(types, list):
            return _ty.Union[tuple([t._python() for t in types])]  # type: ignore
        elif not types:
            return None
        ty = types
        if isinstance(ty, OpenApiType):
            return ty._python()
        ty = ty["type"]
        union = []
        for item in self._raw.get("items", []):
            union.append(item._python())
        if len(union) > 1:
            union = _ty.Union[tuple(union)]  # type: ignore
        elif union:
            union = union[0]
        if "format" in self._raw:
            pass
        match ty:
            case "float":
                ty = float
            case "null":
                ty = None
            case "boolean":
                ty = bool
            case "integer":
                ty = int
            case "string":
                ty = str
            case "array":
                if union:
                    ty = list[union]
                else:
                    ty = list
            case "object":
                if self._obj:
                    ty = self._obj
                else:
                    ty = dict[str]
                pass
            case _:
                raise ValueError(ty)
        return ty


class Paramater(_ty.NamedTuple):
    type: list[OpenApiType]
    description: str
    default: "_ty.Any"
    required: bool

    @classmethod
    def from_param(cls, param: "_core.Parameter", objects: dict):
        param = param or {}
        type = []
        desc = param.get("description", param.get("title", ""))
        required = param.get("required", True)
        type = [OpenApiType(param, objects)]
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
    objects: dict[str, Object]

    def __init__(self, raw: _core.NamespaceInfo) -> None:
        self._raw = raw
        self.methods = {}
        self.objects = _ty.OrderedDict()
        for name, method in self._raw["methods"].items():
            signatures = []
            descr = method["description"]
            returns = []
            args = _ty.OrderedDict()
            for p in method["accepts"]:
                pname = p["name"].replace("-", "_")
                args[pname] = Paramater.from_param(p, self.objects)
            for p in method["returns"]:
                returns.append(Paramater.from_param(p, self.objects))
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
                mem = {}
                code = self.nscodegen.generate(ns)
                if isinstance(code, str):
                    code = [code]
                code, typings, *_ = [*code, None, None]
                ns_path = root / ns.modpath / _INIT
                ns_path.parent.mkdir(exist_ok=True, parents=True)
                ns_path.write_text(code)
                if typings:
                    ns_path.with_suffix(".pyi").write_text(typings)
                index.write(f"from .{ns.module} import {ns.classname}\n")
