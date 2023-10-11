import json
from enum import Enum as _Enum
from pathlib import Path as _P
import re as _re
import keyword as _kw
import typing as _ty
from ..base import TrueNASClient, Namespace
from .. import _utils, _core, api as _api
from dataclasses import dataclass as _dataclass, field as _field

@_dataclass
class PythonNamespaceSignature(_api.NamespaceSignature):
    objects: list[_api.Object|_api.Enum] = _field(default_factory=lambda: [])
    baseclass: Namespace = Namespace
    mixins: list[type] = _field(default_factory=lambda: [])

    @staticmethod
    def from_( ns:_api.NamespaceSignature, baseclass=None, mixins=None) -> 'PythonNamespaceSignature':
        ns = PythonNamespaceSignature(**ns.__dict__, baseclass=baseclass or Namespace, mixins=mixins or [])
        objects = {}
        for method in ns.methods:
            for param in [*method.arguments.values(), *method.returns]:
                for ty in param.type.required_types():
                    if not isinstance(ty, (_api.Object, _api.Enum)) or not ty:
                             continue
                    ty.name = _utils.classname(ty.name).rstrip("_")
                    if not ty.name:
                        if isinstance(ty, _api.Object):
                            ty.name = _utils.classname(f"{method.name}Properties").rstrip("_")
                        else:
                            ty.name = _utils.classname(f"{method.name}Options").rstrip("_")
                    while ty.name in objects and not objects[ty.name].__eq__(ty):
                        ty.name += "_"
                    objects[ty.name] = ty
        ns.objects = list(objects.values())
        return ns

    @property
    def dotname(self):
        return self.name

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
            self.dotname[0].upper()
            + _re.sub("\.[a-z]", lambda m: m.group(0)[1:].upper(), self.dotname)[1:]
        )


class NamespaceCodegen:
    def generate(
        self,
        namespace: _api.NamespaceSignature,
    ) -> tuple[str, str] | str:
        ...


_INIT = "__init__.py"


class Codegen:
    def __init__(self, nscodegen: NamespaceCodegen) -> None:
        self.nscodegen = nscodegen

    def generate(
        self,
        client: TrueNASClient,
        root: _P | str,
        modns: _ty.Callable[[_api.NamespaceSignature], None] = None,
    ):
        root = _P(root)
        root.mkdir(exist_ok=True)
        api = client.api()
        with (root / _INIT).open("w") as index:
            for ns in api.namespaces:
                ns = PythonNamespaceSignature.from_(ns)
                if modns:
                    modns(ns)
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
