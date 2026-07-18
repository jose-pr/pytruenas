from __future__ import annotations

from pathlib import Path as _P
import shutil
import typing as _ty
import functools as _ftools
from ..models import apidump as _api, jsonschema as _schema
from duho import qualname as _qn
from duho import text as _text


class _Missing:
    """Sentinel: a parameter has no default at all (distinct from a ``None``
    default, which is a real, emittable value)."""


_MISSING = _Missing()


def _camelcase(name: str) -> str:
    """CamelCase a single identifier, tolerating empty/trailing segments.

    Splits on ``.``/``_``/``-`` and drops empty parts, so a ``pysafe`` output like
    ``global_`` becomes ``Global``. duho 0.3.0 fixed ``text.camelcase``'s
    trailing-separator crash, so this is now belt-and-suspenders on that front;
    it is kept because it is a one-liner and the empty-part handling is exactly
    what the codegen names (which may carry pysafe suffixes) rely on.
    """
    result = name
    for sep in (".", "_", "-"):
        result = "".join(p[:1].upper() + p[1:] for p in result.split(sep) if p)
    return result


def docstring(text: str) -> str:
    """Return ``text`` as the safe *inside* of a ``\"\"\" ... \"\"\"`` docstring.

    Neutralises the two things that break a triple-quoted literal: a backslash
    (would start an escape) and an embedded/trailing ``"`` run (would close the
    string early -- e.g. a doc ending ``Always returns "pong"`` produced
    ``"pong\"\"\"``). Also drops null bytes, which are a hard ``SyntaxError``
    ("source code string cannot contain null bytes") and appear in some dumps.
    """
    text = (text or "").replace("\x00", "")
    text = text.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    if text.endswith('"'):
        text = text[:-1] + '\\"'
    return text


def _default_literal(default: object) -> str:
    """Render a schema default as a valid Python default-value expression.

    Schema defaults arrive either as already-Python-source strings (the
    synthetic ``_create``/``_update`` helpers pass e.g. ``"None"``) or as raw
    JSON values from the real dump (``[]``, ``{}``, ``""``, ``True``, numbers,
    nested dicts). A plain ``f"={default}"`` mis-renders every non-string JSON
    value (an empty string became ``=`` with nothing after it; a dict became an
    unparenthesised ``{...}``; ``None``/booleans leaked JSON casing). This
    normalises to a literal that always parses.
    """
    if default is ... or default is _MISSING:
        return "..."
    if isinstance(default, str):
        stripped = default.strip()
        # A default already written as Python source (the synthetic helpers, or
        # a schema author who wrote ``"None"``/``"[]"``) is used verbatim when it
        # parses; otherwise it is a genuine string value and gets quoted.
        if stripped in ("None", "True", "False", "...", "[]", "{}"):
            return stripped
        try:
            import ast

            ast.literal_eval(default)
            return default
        except (ValueError, SyntaxError):
            return repr(default)
    # A real JSON value (list/dict/number/bool/None): repr() is valid Python.
    return repr(default)


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
        name = self.name
        typedef = self.type_def(typeddicts)
        if name.startswith("**"):
            # ``**kwargs`` unpacks a TypedDict and can never carry a default --
            # ``**k: T = ...`` is a syntax error.
            return f"{name}:_ty.Unpack[{typedef}]"
        decl = f"{name}:{typedef}"
        default = self.schema.get("default", _MISSING)
        # ``_MISSING`` (key absent) and ``...`` (the synthetic "required"
        # sentinel) both mean "no default" -> emit none.
        if default is not _MISSING and default is not ...:
            decl += f"={_default_literal(default)}"
        return decl

    def type_def(self, typeddicts: dict[str, object]):
        return _schema.Schema.python_declaration(
            self.schema, typeddicts, self.namespace
        )

    @property
    def name(self):
        title = self.schema["title"]  # type:ignore
        # ``**fields``/``__selector`` keep their leading markers; the rest is
        # made a valid Python identifier (``query-filters`` -> ``query_filters``).
        if title.startswith("**") or title.startswith("__"):
            marker, rest = title[:2], title[2:]
            return marker + _text.pysafe(rest)
        return _text.pysafe(title)


class PyDeclaration:
    @property
    def qualname(self) -> _qn.DotQualNamed:
        raise NotImplementedError()

    @_ftools.cached_property
    def pyname(self):
        # ``.new`` runs each dotted part through ``pysafe`` so a namespace named
        # after a keyword (``global`` -> ``global_``) or starting with a digit
        # (a version like ``v26.0.0``) yields valid Python identifiers.
        return _qn.PythonName.new(self.qualname)

    @property
    def classname(self) -> str:
        """CamelCase class/type name for this declaration's last segment.

        Uses :func:`_camelcase` (empty-part-safe) so a ``pysafe``-suffixed name
        like ``global_`` becomes ``Global`` rather than crashing on the trailing
        underscore (see ``duho.text.camelcase`` trailing-separator bug).
        """
        return _camelcase(self.pyname.name)

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

    def declared_parameters(self, typeddicts: dict[str, object]) -> "list[str]":
        """Rendered parameter declarations, valid as a Python signature.

        Once a positional parameter carries a default, every later positional
        parameter must too (``def f(a=1, b)`` is a ``SyntaxError``). Real dumps
        sometimes list an optional param before a required one, so any later
        parameter that lacks its own default is given ``= ...`` (the standard
        stub placeholder). ``*``/``**`` parameters are exempt (they never take a
        positional default and always sort last here).
        """
        decls: "list[str]" = []
        seen_default = False
        for param in self.parameters:
            decl = param.argument_declaration(typeddicts)
            is_var = param.name.startswith("*")
            if not is_var:
                if "=" in decl:
                    seen_default = True
                elif seen_default:
                    decl += "=..."
            decls.append(decl)
        return decls


_ClassInfo = "type | tuple[_ClassInfo, ...]"


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
                update_return = method.definition["schemas"]["properties"]["Return value"]
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
                                "Return value": update_return,
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
                                    "Return value": update_return,
                                },
                            },
                        }
                    )
                    self.childs.append(upsert)

            elif method.qualname.name == "create":
                fields = method.parameters[-4]
                create_return = method.definition["schemas"]["properties"]["Return value"]
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
                                "Return value": create_return,
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
                for name, schema in method.returns.schema["properties"].items():
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
                                            **(idtype or {}),
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
        # The version string (e.g. ``v26.0.0``) is ONE opaque root segment, not a
        # dotted qualname -- collapse its dots so it does not split into three
        # namespace levels with a leaf named ``0`` (an invalid class name).
        version = _qn.DotQualNamed(_text.pysafe(api["version"].replace(".", "_")))
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
            for decl in [*declarations, *namespaces]:
                decl: PyDeclaration
                if decl.qualname.parent == ns and ns != decl:
                    ns.childs.append(decl)
            ns.init()
            # UTF-8 explicitly: docstrings from the dump contain non-ASCII, and
            # the platform default (cp1252 on Windows) would raise or mangle.
            ns_path.write_text(
                renderer.render(ns=ns, path=ns_path, modpath=ns_path.parent),
                encoding="utf-8",
            )
