"""What generate-typings writes, as declarations: namespaces, methods and
their parameters, read from one version of the API definition."""

from __future__ import annotations

import copy as _copy
import functools as _ftools
import logging as _logging
import typing as _ty

from duho import qualname as _qn
from duho import text as _text

from ..models import apidump as _api, jsonschema as _schema
from ..utils import _schema as _read
from . import _types


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
        return _types.declaration(self.schema, typeddicts, self.namespace)

    @property
    def name(self):
        title = self.schema["title"]  # type: ignore
        # ``**fields``/``__selector`` keep their leading markers; the rest is
        # made a valid Python identifier (``query-filters`` -> ``query_filters``).
        if title.startswith("**") or title.startswith("__"):
            marker, rest = title[:2], title[2:]
            return marker + _text.pysafe(rest)
        return _text.pysafe(title)


class Declaration:
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
        """CamelCase class/type name for this declaration's last segment."""
        return _types.class_name(self.pyname.name)

    @property
    def doc(self) -> str:
        return ""

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Declaration):
            return self.qualname == value.qualname
        elif isinstance(value, str):
            return self.qualname == value
        return False


class Method(Declaration):
    #: Describes a runtime `Namespace` helper with a narrower, schema-typed
    #: signature: an incompatible override, deliberately.
    overrides_runtime = False

    def __init__(self, method: _api.APIMethod):
        self.definition = method

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


class Namespace(Declaration):
    childs: list["Declaration"]

    def __init__(self, qualname: _qn.DotQualNamed):
        self._qualname = qualname
        self.childs = []

    @property
    def qualname(self):
        return self._qualname

    def declarations(self, kind: type):
        return sorted(
            [qn for qn in self.childs if isinstance(qn, kind)],
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


def _payload(method: "Method") -> "Parameter | None":
    """The parameter a synthetic helper's ``**fields`` stands for: the payload
    as the ``call`` command finds it (the last object-typed parameter), never a
    call option. ``None`` when the method has no object parameter."""
    index = _read.payload_index(method.definition)
    return None if index is None else method.parameters[index]
