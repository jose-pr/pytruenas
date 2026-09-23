from __future__ import annotations

from pathlib import Path as _P
import copy as _copy
import logging as _logging
import re as _re
import shutil
import tempfile
import typing as _ty
import functools as _ftools
from ..models import apidump as _api, jsonschema as _schema
from duho import qualname as _qn
from duho import text as _text


class _Missing:
    """Sentinel: a parameter has no default at all (distinct from a ``None``
    default, which is a real, emittable value)."""


#: Generation is a library call; it has no host logger to borrow.
_LOGGER = _logging.getLogger("pytruenas.codegen")

_MISSING = _Missing()


class Source(str):
    """A default that is already Python SOURCE, not a string value.

    The synthetic helpers below emit defaults like ``None``; everything coming
    from the API dump is data. Without this marker the two were told apart by
    trying to parse the string, which quietly turned a default of ``"0"`` into
    the integer ``0``.
    """


def _camelcase(name: str) -> str:
    """CamelCase a single identifier, tolerating empty/trailing segments.

    Splits on ``.``/``_``/``-`` and drops empty parts, so a ``pysafe`` output like
    ``global_`` becomes ``Global``. duho 0.3.0 fixed ``text.camelcase``'s
    trailing-separator crash, so this is now belt-and-suspenders on that front;
    it is kept because it is a one-liner and the empty-part handling is exactly
    what the codegen names (which may carry pysafe suffixes) rely on.
    """
    # Every non-alphanumeric character is a word boundary (underscore
    # included -- `\W` treats it as a word character) -- a real dump has
    # titles like "Filesystem Count", "query-options", "acl(nfs4)" and
    # "smb:share"; parens, colons, quotes and brackets used to survive into the
    # name. A leading digit gets a prefix, since no identifier may start with
    # one.
    parts = [part for part in _re.split(r"[^0-9A-Za-z]+", name) if part]
    result = "".join(part[:1].upper() + part[1:] for part in parts)
    if not result:
        return "Unnamed"
    return f"N{result}" if result[0].isdigit() else result


def docstring(text: str) -> str:
    """Return ``text`` as the safe *inside* of a ``\"\"\" ... \"\"\"`` docstring.

    Neutralises the two things that break a triple-quoted literal: a backslash
    (would start an escape) and an embedded/trailing ``"`` run (would close the
    string early -- e.g. a doc ending ``Always returns "pong"`` produced
    ``"pong\"\"\"``). Also drops null bytes, which are a hard ``SyntaxError``
    ("source code string cannot contain null bytes") and appear in some dumps.
    """
    text = (text or "").replace("\x00", "")
    # Every double quote, not just a `"""` run or a single trailing one: a doc
    # ending in `"""` produced `\"\"\\"`, which does not compile at all.
    # Escaping them all is correct for any position and needs no special case.
    return text.replace("\\", "\\\\").replace('"', '\\"')


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
    if isinstance(default, Source):
        # Python source this package wrote itself (a synthetic helper's `None`).
        return str(default)
    if isinstance(default, str):
        # A plain string from the dump is a STRING VALUE. It used to be handed
        # to ast.literal_eval and returned verbatim when that parsed, so a
        # default of "0" became the int literal 0 and "true"/"None" changed
        # meaning -- the stub then disagreed with the API about the type.
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
            schema = {"type": __schema}  # type: ignore
        else:
            schema = __schema

        #: Rendered after a ``*`` separator, i.e. not positional. The call
        #: options are keyword-only at runtime, so a stub that offered them
        #: positionally invited a call that shifts a real parameter.
        self.keyword_only = False
        self.namespace = __namespace or _qn.PythonName("")
        self.schema = _ty.cast(_schema.Schema, schema or {})
        self.schema.update(kwargs)  # type: ignore

    def argument_declaration(self, typeddicts: dict[str, object]):
        name = self.name
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
    def qualname(self):  # type: ignore
        return _qn.DotQualNamed(self.definition["name"])

    @property
    def doc(self):
        doc = self.definition["doc"] or ""
        return doc.split(".. examples", maxsplit=1)[0].strip()

    @_ftools.cached_property
    def parameters(self) -> list[Parameter]:
        callparams = self.definition["schemas"]["properties"]["Call parameters"]
        items = callparams["prefixItems"]  # type: ignore
        params = []
        for item in items:
            params.append(Parameter(item, self.pyname.relative_to(self.pyname.parent)))

        if not self.pyname.name.startswith("_"):
            # The call options `Namespace.__call__` accepts. They are
            # KEYWORD-ONLY in the stub (the `*` below): the runtime takes
            # middleware parameters positionally and raises TypeError for any
            # other keyword, so a stub offering these positionally invited a
            # call that shifts a real parameter. `_timeout` and `_tries` were
            # missing entirely.
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
                    title="_tries",
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
        star_emitted = False
        for param in self.parameters:
            if getattr(param, "keyword_only", False) and not star_emitted:
                # Everything after this is keyword-only, which also ends the
                # "a default must follow a default" rule.
                decls.append("*")
                star_emitted = True
                seen_default = False
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
                update_return = method.definition["schemas"]["properties"][
                    "Return value"
                ]
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
                                            "_name": fields.name,  # type: ignore
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
                                                "_name": fields.name,  # type: ignore
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
                create_return = method.definition["schemas"]["properties"][
                    "Return value"
                ]
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
                                            "_name": fields.name,  # type: ignore
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
                idtype = None
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
                                            "_name": "get",  # type: ignore
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
#: Written into every generated tree, so a later run knows it may replace it.
_MARKER = ".pytruenas-typings"


def _check_replaceable(root: _P) -> None:
    """Refuse to replace a directory that is not a typings tree.

    Replaceable: absent, empty, carrying the marker, or holding nothing but
    ``.pyi`` stubs (a tree generated before the marker existed). Anything else
    -- a checkout's ``.git``, source files, notes -- is someone's data.
    """
    if not root.exists():
        return
    if not root.is_dir():
        raise FileExistsError(f"{root} exists and is not a directory")
    if (root / _MARKER).exists():
        return
    foreign = next(
        (p for p in root.rglob("*") if p.is_file() and p.suffix != ".pyi"), None
    )
    if foreign is not None:
        raise FileExistsError(
            f"refusing to replace {root}: it is not a typings tree "
            f"({foreign.relative_to(root)} is not a stub); choose another path"
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
        # A copy: this used to prefix the method names of the CALLER's dump
        # (`user.query` -> `v26_0_0.user.query`) and overwrite its return
        # titles, so a caller generating twice from one dump got different
        # output the second time.
        api = _copy.deepcopy(api)
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
                # A middleware method whose name is also a real `Namespace`
                # method (`core.subscribe` vs `Namespace.subscribe`). Emitting
                # it redefined the class member, so a checker accepted
                # `ns.subscribe(event)` -- which at runtime calls the REAL
                # method with a positional callback -- and rejected the correct
                # `ns.subscribe()`. The runtime way to reach the middleware one
                # is `ns(_method="subscribe", ...)`, which needs no stub.
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
        try:
            from . import jinja
        except ImportError as exc:
            raise ImportError(
                "generating typings needs jinja2: pip install pytruenas[codegen]"
            ) from exc
        # Render into a sibling first and swap it in only once every stub is
        # written: a failure part-way leaves the previous output untouched.
        final.parent.mkdir(parents=True, exist_ok=True)
        root = _P(tempfile.mkdtemp(prefix=f".{final.name}.", dir=final.parent))
        try:
            self._render(jinja, version, declarations, namespaces, root)
            (root / _MARKER).write_text(
                "Generated by `pytruenas generate-typings`; replaced on regeneration.\n",
                encoding="utf-8",
            )
        except BaseException:
            shutil.rmtree(root, ignore_errors=True)
            raise
        if final.exists():
            shutil.rmtree(final)
        root.rename(final)

    @staticmethod
    def _render(jinja, version, declarations, namespaces, root: _P) -> None:
        renderer = jinja.Renderer("namespace.pyi")
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
                renderer.render(
                    ns=ns,
                    path=ns_path,
                    modpath=ns_path.parent,
                    # The root module also gets the documented `Current` alias:
                    # the generated class is named after the version (V26000),
                    # so `TrueNASClient[Current]` had nothing to resolve to.
                    alias="Current" if ns.qualname == version else None,
                ),
                encoding="utf-8",
            )
