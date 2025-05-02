from pathlib import Path as _P
import shutil
import typing as _ty
import functools as _ftools
from ..models import apidump as _api, jsonschema as _schema
from ..utils import qualname as _qn


class Parameter:
    def __init__(
        self,
        __schema: _schema.Schema | None | str = None,
        __namespace: _qn.PythonName | None = None,
        **kwargs,
    ):

        if isinstance(__schema, str):
            schema = {
                "type": __schema  # type:ignore
            }
        else:
            schema = __schema

        self.namespace = __namespace or _qn.PythonName("")
        self.schema = _ty.cast(_schema.Schema, schema or {})
        self.schema.update(kwargs)  # type:ignore

    def argument_declaration(self, typeddicts: dict[str, object]):
        decl = self.name
        typedef = self.type_def(typeddicts)
        if self.name.startswith("**"):
            typedef = f"_ty.Unpack[{typedef}]"
        decl += f":{typedef}"
        default = self.schema.get("default", ...)
        if default != ...:
            decl += f"={default}"
        return decl

    def type_def(self, typeddicts: dict[str, object]):
        return _schema.Schema.python_declaration(
            self.schema, typeddicts, self.namespace
        )

    @property
    def name(self):
        name = self.schema["title"]  # type:ignore
        return name


class PyDeclaration:
    @property
    def qualname(self) -> _qn.DotQualNamed:
        raise NotImplementedError()

    @_ftools.cached_property
    def pyname(self):
        return _qn.PythonName(self.qualname)

    @property
    def doc(self) -> str:
        return ""

    def __eq__(self, value: object) -> bool:
        if isinstance(value, PyDeclaration):
            return self.qualname == value.qualname
        elif isinstance(value, str):
            return self.qualname == value
        return False

    def clear_cache(self):
        for name, attr in type(self).__dict__.items():
            if isinstance(attr, _ftools.cached_property):
                if name in self.__dict__:
                    del self.__dict__[name]


class Method(PyDeclaration):
    def __init__(self, method: _api.Method):
        self.definition = method

    @property
    def definition(self):
        return self._definition

    @definition.setter
    def definition(self, value: _api.Method):
        self._definition = value
        self.clear_cache()

    @_ftools.cached_property
    def qualname(self):  # type:ignore
        return _qn.DotQualNamed(self.definition["name"])

    @property
    def doc(self):
        doc = self.definition["doc"] or ""
        return doc.split(".. examples", maxsplit=1)[0].strip()

    @_ftools.cached_property
    def parameters(self) -> list[Parameter]:
        callparams = self.definition["schemas"]["properties"]["Call parameters"]
        items = callparams["prefixItems"]  # type:ignore
        params = []
        for item in items:
            params.append(Parameter(item, self.pyname.relative_to(self.pyname.parent)))

        # _ty.Sequence[str] | None | _q._Exclude
        if not self.pyname.name.startswith("_"):
            params.extend(
                [
                    Parameter(
                        {},
                        self.pyname,
                        title="_method",
                        anyOf=["string", "null"],
                        default="None",
                    ),
                    Parameter(
                        {},
                        self.pyname,
                        title="_ioerror",
                        type="boolean",
                        default="False",
                    ),
                    Parameter(
                        {},
                        self.pyname,
                        title="_filetransfer",
                        anyOf=["boolean", "!bytes"],
                        default="False",
                    ),
                ]
            )
        return params

    @_ftools.cached_property
    def returns(self):
        returns = self.definition["schemas"]["properties"]["Return value"]
        return Parameter(
            returns, self.pyname.relative_to(self.pyname.parent), title="return"
        )


_ClassInfo: _ty.TypeAlias = "type | tuple[_ClassInfo, ...]"


class Namespace(PyDeclaration):
    childs: list["PyDeclaration"]

    def __init__(self, qualname: _qn.DotQualNamed):
        self._qualname = qualname
        self.childs = []

    @property
    def qualname(self):
        return self._qualname

    def declarations(self, type: _ClassInfo):
        return sorted(
            [qn for qn in self.childs if isinstance(qn, type)],
            key=lambda qn: qn.qualname,
        )

    def namespaces(self):
        return self.declarations(Namespace)

    def methods(self):
        return _ty.cast(list[Method], self.declarations(Method))

    def init(self):
        for method in self.methods():
            if method.qualname.name == "update":
                fields = method.parameters[-4]
                idtype = None
                for param in method.parameters:
                    if param.name == "id":
                        idtype = {
                            "anyOf": [
                                param.schema.get("type", "!str|int"),
                                "!_ty.Sequence[str]",
                            ]
                        }
                update = Method(
                    {
                        "name": "_update",
                        "roles": method.definition["roles"],
                        "doc": "",
                        "schemas": {
                            "type": "object",
                            "properties": {
                                "Call parameters": {
                                    "type": "array",
                                    "prefixItems": [
                                        {
                                            "title": "__selector",
                                            **(idtype or {}),
                                            "default": (
                                                ... if idtype is not None else None
                                            ),
                                        },
                                        {
                                            **fields.schema,
                                            "title": "**fields",
                                            "_name": fields.name,  # type:ignore
                                        },
                                    ],
                                    "items": True,
                                },
                                "Return value": "!UpdateReturn",
                            },
                        },
                    }
                )
                self.childs.append(update)
                if idtype:
                    upsert = Method(
                        {
                            "name": "_upsert",
                            "roles": method.definition["roles"],
                            "doc": "",
                            "schemas": {
                                "type": "object",
                                "properties": {
                                    "Call parameters": {
                                        "type": "array",
                                        "prefixItems": [
                                            {
                                                "title": "__selector",
                                                **(idtype or {}),
                                                "default": (
                                                    ... if idtype is not None else None
                                                ),
                                            },
                                            {
                                                **fields.schema,
                                                "title": "**fields",
                                                "_name": fields.name,  # type:ignore
                                            },
                                        ],
                                        "items": True,
                                    },
                                    "Return value": "!UpdateReturn",
                                },
                            },
                        }
                    )
                    self.childs.append(upsert)

            elif method.qualname.name == "create":
                fields = method.parameters[-4]
                update = Method(
                    {
                        "name": "_create",
                        "roles": method.definition["roles"],
                        "doc": "",
                        "schemas": {
                            "type": "object",
                            "properties": {
                                "Call parameters": {
                                    "type": "array",
                                    "prefixItems": [
                                        {
                                            **fields.schema,
                                            "title": "**fields",
                                            "_name": fields.name,  # type:ignore
                                        },
                                    ],
                                    "items": True,
                                },
                                "Return value": "!CreateReturn",
                            },
                        },
                    }
                )
                self.childs.append(update)
            elif method.qualname.name == "get_instance":
                for param in method.parameters:
                    if param.name == "id":
                        idtype = {
                            "anyOf": [
                                param.schema.get("type", "!str|int"),
                                "!_ty.Sequence[str]",
                                "!None",
                            ]
                        }
                props = {}
                for name, schema in method.returns.schema[
                    "properties"
                ].items():  # type:ignore
                    schema = {**schema}
                    schema["required"] = False
                    props[name] = schema
                update = Method(
                    {
                        "name": "_get",
                        "roles": method.definition["roles"],
                        "doc": "",
                        "schemas": {
                            "type": "object",
                            "properties": {
                                "Call parameters": {
                                    "type": "array",
                                    "prefixItems": [
                                        {
                                            "title": "__id_or_filter",
                                            **(idtype or {}),  # type:ignore
                                            "default": None,
                                        },
                                        {
                                            "type": "object",
                                            "properties": props,
                                            "title": "**fields",
                                            "_name": "get",  # type:ignore
                                        },
                                    ],
                                    "items": True,
                                },
                                "Return value": "!GetInstanceReturn|None",
                            },
                        },
                    }
                )
                self.childs.append(update)


class Renderer:
    def __init__(self, template: str): ...
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
        declarations: list[PyDeclaration] = []
        version = _qn.DotQualNamed(api["version"])
        version_ns = Namespace(version)
        for method in api["methods"]:
            method["name"] = version / method["name"]
            declarations.append(Method(method))

        namespaces: list[Namespace] = [version_ns]
        for decl in declarations:
            while True:
                namespace = decl.qualname.parent
                if namespace and namespace not in namespaces:
                    decl = Namespace(namespace)
                    namespaces.append(decl)
                else:
                    break

        root = _P(root)
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(exist_ok=True, parents=True)
        from . import jinja

        renderer = jinja.Renderer("namespace.pyi")
        for ns in sorted(namespaces, key=lambda ns: ns.qualname):
            ns_path = ns.pyname.relative_to(version).as_path(root) / _INIT
            ns_path.parent.mkdir(exist_ok=True, parents=True)
            with (ns_path).open("w") as ns_index:
                for decl in [*declarations, *namespaces]:
                    decl: PyDeclaration
                    if decl.qualname.parent == ns and ns != decl:
                        ns.childs.append(decl)
                ns.init()
                ns_index.write(
                    renderer.render(ns=ns, path=ns_path, modpath=ns_path.parent)
                )
