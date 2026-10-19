from __future__ import annotations

from pathlib import Path as _P
import copy as _copy
import json as _json
import logging as _logging
import os as _os
import shutil
import tempfile
import time as _time
import typing as _ty
import functools as _ftools
from ..models import apidump as _api, jsonschema as _schema
from ..utils import _schema as _read
from duho import qualname as _qn
from duho import text as _text


class _Missing:
    """Sentinel: a parameter has no default at all (distinct from a ``None``
    default, which is a real, emittable value)."""


#: Generation is a library call; it has no host logger to borrow.
_LOGGER = _logging.getLogger("pytruenas.codegen")

_MISSING = _Missing()


class Source(str):
    """A default that is already Python SOURCE, not a string value: what the
    synthetic helpers and call options write (``None``, ``False``). Every
    default from the API dump is data, rendered with ``repr``."""


def _camelcase(name: str) -> str:
    """CamelCase a dump name into a class name.

    Every non-alphanumeric character, underscore included, separates two words
    and empty parts are dropped: ``global_`` (a ``pysafe`` output) becomes
    ``Global`` and ``acl(nfs4)`` ``AclNfs4``. A leading digit gets an ``N``.
    """
    parts = _read.words(name)
    result = "".join(part[:1].upper() + part[1:] for part in parts)
    if not result:
        return "Unnamed"
    return f"N{result}" if result[0].isdigit() else result


def docstring(text: str) -> str:
    """Return ``text`` as the safe *inside* of a ``\"\"\" ... \"\"\"`` docstring.

    Escapes every backslash (it would start an escape) and every ``"`` (three
    in a row, or one at the end, close the literal early), and drops null
    bytes, which no source file may contain and some dumps do.
    """
    text = (text or "").replace("\x00", "")
    return text.replace("\\", "\\\\").replace('"', '\\"')


def _default_literal(default: object) -> str:
    """Render a schema default as a Python default-value expression.

    A :class:`Source` is emitted as written. Anything else is a JSON value
    from the dump, and ``repr`` renders it as a literal of the same type: the
    string ``"0"`` stays ``'0'``, never the integer ``0``.
    """
    if default is ... or default is _MISSING:
        return "..."
    if isinstance(default, Source):
        return str(default)
    return repr(default)


class Parameter:
    def __init__(
        self,
        __schema: _schema.Schema | None | str = None,
        __namespace: _qn.PythonName | None = None,
        **kwargs,
    ):

        if isinstance(__schema, str):
            schema = {"type": __schema}  # type: ignore
        else:
            schema = __schema

        #: Rendered after a ``*`` separator, i.e. not positional: the call
        #: options are keyword-only at runtime.
        self.keyword_only = False
        self.namespace = __namespace or _qn.PythonName("")
        self.schema = _ty.cast(_schema.Schema, schema or {})
        self.schema.update(kwargs)  # type: ignore

    def argument_declaration(
        self, typeddicts: dict[str, object], name: "str | None" = None
    ):
        name = name or self.name
        typedef = self.type_def(typeddicts)
        if name.startswith("**"):
            # ``**kwargs`` unpacks a TypedDict and can never carry a default --
            # ``**k: T = ...`` is a syntax error.
            return f"{name}:_Unpack[{typedef}]"
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
        title = self.schema["title"]  # type: ignore
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
        """CamelCase class/type name for this declaration's last segment
        (see :func:`_camelcase`)."""
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
    #: Describes a runtime `Namespace` helper with a narrower, schema-typed
    #: signature: an incompatible override, deliberately.
    overrides_runtime = False

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
    def qualname(self):  # type: ignore
        return _qn.DotQualNamed(self.definition["name"])

    @property
    def doc(self):
        doc = self.definition["doc"] or ""
        return doc.split(".. examples", maxsplit=1)[0].strip()

    @_ftools.cached_property
    def parameters(self) -> list[Parameter]:
        params = []
        for index, item in enumerate(_read.parameters(self.definition)):
            if not item.get("title"):
                # The name `help` shows for an untitled parameter.
                item = {**item, "title": f"arg{index + 1}"}
            params.append(Parameter(item, self.pyname.relative_to(self.pyname.parent)))

        if not self.pyname.name.startswith("_"):
            # The call options `Namespace.__call__` accepts, keyword-only (the
            # `*` below) as at runtime, which takes middleware parameters
            # positionally and raises TypeError for any other keyword.
            options = [
                Parameter(
                    {},
                    self.pyname,
                    title="_method",
                    anyOf=["string", "null"],
                    default=Source("None"),
                ),
                Parameter(
                    {},
                    self.pyname,
                    title="_ioerror",
                    type="boolean",
                    default=Source("False"),
                ),
                Parameter(
                    {},
                    self.pyname,
                    title="_filetransfer",
                    anyOf=["boolean", "!bytes"],
                    default=Source("False"),
                ),
                Parameter(
                    {},
                    self.pyname,
                    title="_timeout",
                    anyOf=["number", "null"],
                    default=Source("..."),
                ),
                Parameter(
                    {},
                    self.pyname,
                    title="_retries",
                    type="integer",
                    default=Source("1"),
                ),
            ]
            for option in options:
                option.keyword_only = True
            params.extend(options)
        return params

    @_ftools.cached_property
    def returns(self):
        returns = _read.returns(self.definition)
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
        star_emitted = False
        # Two titles can sanitize to one name (`a-b`, `a_b`) and a title can be
        # `self`; either is a duplicate argument, which `compile()` rejects.
        used = {"self"}
        for param in self.parameters:
            if getattr(param, "keyword_only", False) and not star_emitted:
                # Everything after this is keyword-only, which also ends the
                # "a default must follow a default" rule.
                decls.append("*")
                star_emitted = True
                seen_default = False
            name = param.name
            bare = name.lstrip("*")
            unique = bare
            while unique in used:
                unique += "_"
            used.add(unique)
            decl = param.argument_declaration(
                typeddicts, name[: len(name) - len(bare)] + unique
            )
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
            name = method.qualname.name
            if name == "get_instance":
                self._add_get(method)
                continue
            if name not in ("update", "create"):
                continue
            fields = _payload(method)
            if fields is None:
                # `**fields` must unpack a TypedDict, and this method takes no
                # object payload to build one from: the runtime helper's own
                # signature is left to describe it.
                _LOGGER.info(
                    "%s has no object payload; no _%s stub emitted",
                    method.definition["name"],
                    name,
                )
                continue
            payload = {**fields.schema, "title": "**fields", "_name": fields.name}
            ret = _read.returns(method.definition)
            if name == "create":
                self.childs.append(_helper(method, "_create", [payload], ret))
                continue
            idtype = _id_type(method)
            selector = {
                "title": "__selector",
                **(idtype or {}),
                "default": ... if idtype is not None else None,
            }
            self.childs.append(_helper(method, "_update", [selector, payload], ret))
            if idtype:
                self.childs.append(
                    _helper(method, "_upsert", [dict(selector), dict(payload)], ret)
                )

    def _add_get(self, method: "Method") -> None:
        returned = method.returns.schema
        props = _read.properties(returned)
        if props is None:
            # The filter keywords are the returned object's properties; with
            # none to read, the runtime helper's own signature describes it.
            _LOGGER.info(
                "%s returns no object with properties; no _get stub emitted",
                method.definition["name"],
            )
            return
        if returned.get("properties"):
            # The TypedDict that `get_instance`'s own return renders to.
            ret: object = "!GetInstanceReturn|None"
        else:
            # A union (`anyOf[object, null]`), rendered again under `_get`.
            members = _copy.deepcopy(returned.get("anyOf") or returned.get("oneOf"))
            if not any(
                isinstance(m, dict) and m.get("type") == "null" for m in members
            ):
                members.append({"type": "null"})
            ret = {"anyOf": members}
        idtype = _id_type(method, "!None")
        filters = {
            "type": "object",
            "properties": {
                prop: {**schema, "required": False} for prop, schema in props.items()
            },
            "title": "**fields",
            "_name": "get",
        }
        selector = {"title": "__id_or_filter", **(idtype or {}), "default": None}
        self.childs.append(_helper(method, "_get", [selector, filters], ret))


def _id_type(method: "Method", *extra: str) -> "dict | None":
    """A synthetic helper's selector type: the method's `id` parameter's type
    or a list of filters; ``None`` when it has no `id` parameter."""
    for param in method.parameters:
        if param.name == "id":
            return {
                "anyOf": [
                    param.schema.get("type", "!str|int"),
                    "!_ty.Sequence[str]",
                    *extra,
                ]
            }
    return None


def _helper(method: "Method", name: str, params: list, ret: object) -> "Method":
    """A synthetic method entry describing a runtime `Namespace` helper."""
    helper = Method(
        {
            "name": name,
            "roles": method.definition.get("roles") or [],
            "doc": "",
            "schemas": {
                "type": "object",
                "properties": {
                    _read.CALL_PARAMS: {
                        "type": "array",
                        "prefixItems": params,
                        "items": True,
                    },
                    _read.RETURN: ret,
                },
            },
        }
    )
    helper.overrides_runtime = True
    return helper


#: The start of every stub module, up to its child-namespace imports.
_HEADER = """\
from __future__ import annotations

from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import sys
import typing as _ty

# Never, NotRequired and Unpack are typing members only from 3.11; this
# project's floor -- and so a consumer's checking target -- is 3.9. `sys` is not
# aliased: mypy reads a version check only on the module's own name.
if sys.version_info >= (3, 11):
    from typing import Never as _Never, NotRequired as _NotRequired, Unpack as _Unpack
else:
    from typing_extensions import (
        Never as _Never,
        NotRequired as _NotRequired,
        Unpack as _Unpack,
    )"""

#: Ends the root module: `TrueNASClient[Current]` is the documented spelling.
_CURRENT = """

#: The documented spelling: `TrueNASClient[Current]`, so a consumer pins "the
#: version these typings were generated from" without naming it.
{alias} = {classname}"""


def _render(ns: "Namespace", alias: "_ty.Optional[str]" = None) -> str:
    """The source of one namespace's stub module.

    ``alias``, given for the root namespace only, names an alias of its class.
    TypedDicts are collected while the signatures are rendered, so they follow
    the class.
    """
    typeddicts: "dict[str, dict[str, str]]" = {}
    out = [_HEADER]
    children = ns.namespaces()
    for child in children:
        module = child.pyname.relative_to(ns.pyname)
        out.append(f"\nfrom .{module} import {child.classname}")
    out.append(f"\n\n\nclass {ns.classname}(_NS):\n    ")
    methods = ns.methods()
    for method in methods:
        ignore = "  # type: ignore[override]" if method.overrides_runtime else ""
        out.append(f"\n    def {method.pyname.name}(self,{ignore}")
        out.extend(
            f"\n        {decl}," for decl in method.declared_parameters(typeddicts)
        )
        returns = method.returns.type_def(typeddicts)
        out.append(f'\n    ) -> {returns}:\n        """{docstring(method.doc)}"""')
        out.append("\n        ...")
    for child in children:
        out.append(f"\n    {child.pyname.name}: {child.classname}")
    if not methods and not children:
        out.append("\n    pass")
    out.append("\n\n")
    for name, properties in typeddicts.items():
        out.append(f"\n{name} = _ty.TypedDict('{name}', {{")
        # JSON string syntax is valid Python string syntax.
        out.extend(
            f"\n    {_json.dumps(key)}: {value}," for key, value in properties.items()
        )
        out.append("\n})\n")
    if alias:
        out.append(_CURRENT.format(alias=alias, classname=ns.classname))
    return "".join(out)


_INIT = "__init__.pyi"
#: Written into every generated tree, so a later run knows it may replace it.
_MARKER = ".pytruenas-typings"


def _payload(method: "Method") -> "Parameter | None":
    """The parameter a synthetic helper's ``**fields`` stands for: the payload
    as the ``call`` command finds it (the last object-typed parameter), never a
    call option. ``None`` when the method has no object parameter."""
    index = _read.payload_index(method.definition)
    return None if index is None else method.parameters[index]


def _check_replaceable(root: _P) -> None:
    """Refuse to replace a directory that is not a typings tree.

    Replaceable: absent, empty, or carrying the marker every generated tree
    has. Anything else is someone's data -- a checkout's ``.git``, notes, or
    hand-written stubs (``typings/`` is where pyright looks for them).
    """
    if not root.exists():
        return
    if not root.is_dir():
        raise FileExistsError(f"{root} exists and is not a directory")
    if (root / _MARKER).exists() or next(root.iterdir(), None) is None:
        return
    raise FileExistsError(
        f"refusing to replace {root}: it is not a tree generate-typings wrote "
        f"(no {_MARKER}); choose another path"
    )


def _runtime_namespace_attributes() -> "frozenset[str]":
    """Names a generated namespace class must not redefine.

    The real `Namespace` methods (`subscribe`, and the `_query`/`_get`/...
    helpers, which are generated deliberately from the schema and so are
    excluded by the caller).
    """
    from ..namespace import Namespace as _RuntimeNamespace

    return frozenset(
        name for name in dir(_RuntimeNamespace) if not name.startswith("__")
    )


def _shadows_runtime(declaration: "Method") -> bool:
    """Whether this dump method would redefine a real ``Namespace`` member."""
    name = declaration.pyname.name
    if name.startswith("_"):
        # The synthetic helpers are meant to describe the runtime ones.
        return False
    return name in _runtime_namespace_attributes()


def _swap(new: _P, final: _P) -> None:
    """Put the tree ``new`` at ``final``.

    The previous tree is renamed aside and deleted only once ``new`` is in
    place, so a failure (on Windows, a stub held open or a shell inside the
    tree) leaves it whole at ``final``.
    """
    old = None
    if final.exists():
        old = new.with_name(new.name + ".old")
        _rename(final, old)
    try:
        _rename(new, final)
    except BaseException:
        if old is not None:
            try:
                _rename(old, final)
            except OSError:
                _LOGGER.error("the previous output is left at %s", old)
        raise
    if old is not None:
        shutil.rmtree(old, ignore_errors=True)
        if old.exists():
            _LOGGER.warning("could not delete the previous output at %s", old)


def _rename(source: _P, target: _P) -> None:
    """``source.rename(target)``, retried for about a second on Windows, where
    a scanner or indexer opening a file just written fails it briefly."""
    attempts = 5 if _os.name == "nt" else 1
    for attempt in range(attempts):
        try:
            source.rename(target)
            return
        except PermissionError:
            if attempt == attempts - 1:
                raise
            _time.sleep(0.05 * 2**attempt)


def _empty_arrays(node: object) -> None:
    """Rewrite ``items: false`` in place, so that the stub names the template's
    ``_Never`` (``typing`` has ``Never`` only from 3.11) whatever interpreter
    generates it. With ``prefixItems`` it closes a tuple: any JSON array."""
    if isinstance(node, dict):
        if node.get("items") is False:
            if "prefixItems" in node:
                del node["items"]
            else:
                node["items"] = {"type": "!_Never"}
        for value in node.values():
            _empty_arrays(value)
    elif isinstance(node, list):
        for value in node:
            _empty_arrays(value)


def _check_inside(root: _P, path: _P) -> None:
    """Refuse a generated path that escapes ``root``.

    Every component of it comes from the API dump (namespace and method names),
    so a name carrying a separator or a ``..`` would otherwise write outside the
    output directory.
    """
    try:
        resolved = path.resolve()
        resolved.relative_to(root.resolve())
    except ValueError:
        raise BadApiName(f"{path} would be written outside {root}") from None


class BadApiName(ValueError):
    """A name from the API dump cannot be used as a Python/file name."""


class Codegen:
    def __init__(self) -> None: ...
    def generate(
        self,
        api: _api.Version,
        root: _P | str,
    ):
        # A copy: method names are prefixed and return titles rewritten below,
        # and the caller's dump must come back as it was given.
        api = _copy.deepcopy(api)
        _empty_arrays(api)
        declarations: list[PyDeclaration] = []
        # The version string (e.g. ``v26.0.0``) is ONE opaque root segment, not a
        # dotted qualname -- collapse its dots so it does not split into three
        # namespace levels with a leaf named ``0`` (an invalid class name).
        version = _qn.DotQualNamed(_text.pysafe(api["version"].replace(".", "_")))
        version_ns = Namespace(version)
        for method in api["methods"]:
            method["name"] = version / method["name"]
            declaration = Method(method)
            if _shadows_runtime(declaration):
                # A middleware method named like a real `Namespace` method
                # (`core.subscribe`): a stub would redefine the class member, and
                # a checker would type the runtime method with the middleware's
                # signature. `ns(_method="subscribe", ...)` reaches it.
                _LOGGER.info(
                    "%s is shadowed by Namespace.%s; call it as "
                    '_method="%s" (no stub emitted)',
                    method["name"],
                    declaration.pyname.name,
                    declaration.pyname.name,
                )
                continue
            declarations.append(declaration)

        namespaces: list[Namespace] = [version_ns]
        for decl in declarations:
            while True:
                namespace = decl.qualname.parent
                if namespace and namespace not in namespaces:
                    decl = Namespace(namespace)
                    namespaces.append(decl)
                else:
                    break

        final = _P(root)
        _check_replaceable(final)
        # Render into a sibling first and swap it in only once every stub is
        # written: a failure part-way leaves the previous output untouched.
        final.parent.mkdir(parents=True, exist_ok=True)
        root = _P(tempfile.mkdtemp(prefix=f".{final.name}.", dir=final.parent))
        try:
            self._write(version, declarations, namespaces, root)
            (root / _MARKER).write_text(
                "Generated by `pytruenas generate-typings`; replaced on regeneration.\n",
                encoding="utf-8",
            )
            _swap(root, final)
        except BaseException:
            shutil.rmtree(root, ignore_errors=True)
            raise

    @staticmethod
    def _write(version, declarations, namespaces, root: _P) -> None:
        for ns in sorted(namespaces, key=lambda ns: ns.qualname):
            ns_path = ns.pyname.relative_to(version).as_path(root) / _INIT
            _check_inside(root, ns_path)
            ns_path.parent.mkdir(exist_ok=True, parents=True)
            for decl in [*declarations, *namespaces]:
                decl: PyDeclaration
                if decl.qualname.parent == ns and ns != decl:
                    ns.childs.append(decl)
            ns.init()
            # UTF-8 explicitly: docstrings from the dump contain non-ASCII, and
            # the platform default (cp1252 on Windows) would raise or mangle.
            ns_path.write_text(
                # The root class is named after the version (`V2600` for
                # v26.0.0); `Current` is the documented name for it.
                _render(ns, alias="Current" if ns.qualname == version else None),
                encoding="utf-8",
            )
