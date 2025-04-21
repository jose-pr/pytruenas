import json
from enum import Enum as _Enum
from pathlib import Path as _P
import re as _re
import keyword as _kw
import shutil
import typing as _ty
from ..models import apidump as _api, jsonschema as _schema


class _QualNamed:
    qualname: str

    def __init__(self):
        pass

    @property
    def name(self):
        return self.qualname.split(".")[-1]

    @property
    def pysafename(self):
        return ".".join(
            [(f"{n}_" if _kw.iskeyword(n) else n) for n in self.qualname.split(".")]
        )

    @property
    def parent(self):
        return ".".join(self.qualname.split(".")[:-1])

    def __eq__(self, value):
        qualname = value if isinstance(value, str) else getattr(value, "qualname", None)
        return self.qualname == qualname

    @property
    def classname(self):
        qualname = self.qualname
        return (
            qualname[0].upper()
            + _re.sub("\.[a-z]", lambda m: m.group(0)[1:].upper(), qualname)[1:]
        )

    @property
    def methodname(self):
        return self.pysafename.split(".")[-1]


class Parameter:
    def __init__(self, schema: _schema.Schema):
        self.schema = schema
        self.name = schema["title"]

    def argument_declaration(self):
        return self.name


class Method(_QualNamed):
    def __init__(self, method: _api.Method):
        self.definition = method

    @property
    def qualname(self):
        return self.definition["name"]

    @property
    def doc(self):
        doc = self.definition["doc"] or ""
        return doc.split('.. examples', maxsplit=1)[0].strip()

    def parameters(self) -> dict[str]:
        callparams = self.definition["schemas"]["properties"]["Call parameters"]
        items = callparams["prefixItems"]
        params = []
        for item in items:
            params.append(Parameter(item))
        return params

    def returns(self):
        returns = self.definition["schemas"]["properties"]["Return value"]
        return None


class Namespace(_QualNamed):
    childs: list["_QualNamed"]

    def __init__(self, qualname: str):
        self.qualname = qualname
        self.childs = []

    @property
    def module(self):
        return self.pysafename

    @property
    def modpath(self):
        return _P(self.module.replace(".", "/"))

    def query(self, type: type | _ty.Iterable[type]):
        return sorted(
            [qn for qn in self.childs if isinstance(qn, type)],
            key=lambda qn: qn.qualname,
        )

    def namespaces(self):
        return self.query(Namespace)

    def methods(self):
        return self.query(Method)


class RootNamespace(Namespace):
    def __init__(self, rootname: str):
        self.rootname = rootname
        super().__init__("")

    @property
    def classname(self):
        return self.rootname.capitalize()


class Renderer:
    def render(
        self,
        **ctx,
    ) -> str: ...


_INIT = "__init__.pyi"


class Codegen:
    def __init__(self) -> None: ...
    def generate(
        self,
        api: _api.Version,
        root: _P | str,
    ):
        qualnames: list[_QualNamed] = []
        version = api["version"]
        for method in api["methods"]:
            qualnames.append(Method(method))

        namespaces: list[Namespace] = [RootNamespace(version)]
        for qn in qualnames:
            while True:
                parent = qn.parent
                if parent and parent not in namespaces:
                    qn = Namespace(parent)
                    namespaces.append(qn)
                else:
                    break

        root = _P(root)
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(exist_ok=True, parents=True)
        from . import jinja

        renderer = jinja.NamespaceRenderer()
        for ns in sorted(namespaces, key=lambda ns: ns.qualname):
            ns_path = root / ns.modpath / _INIT
            ns_path.parent.mkdir(exist_ok=True, parents=True)
            with (ns_path).open("w") as ns_index:
                for qn in [*qualnames, *namespaces]:
                    qn: _QualNamed
                    if qn.parent == ns and ns != qn:
                        ns.childs.append(qn)
                ns_index.write(
                    renderer.render(ns=ns, path=ns_path, modpath=ns_path.parent)
                )
