"""Render CLI-style help for a middleware method from the API definition.

The API definition is the only place that records what a method accepts, and
the parts a caller needs most -- a field's description, its default, the values
an enum allows, whether it is required at all -- exist *only* there. Generated
``.pyi`` stubs cannot carry them, which is why help reads the dump (cached by
:mod:`pytruenas.utils.apicache`) rather than the stubs generated from it.

Everything here is a pure function over a dump slice: text in, text out, no
client and no network, so the shapes an appliance actually emits can be pinned
down in tests.

A method's parameters live in ``schemas.properties["Call parameters"]`` as
``prefixItems`` -- positional, in order -- and its result in
``["Return value"]``. A create/update method's payload is a single ``object``
parameter, so its *properties* are what a caller really passes; those become the
``--field=value`` names.
"""

from __future__ import annotations

import textwrap as _textwrap
import typing as _ty

#: Width the descriptions wrap to.
WIDTH = 88

_CALL_PARAMS = "Call parameters"
_RETURN = "Return value"


class UnknownMethod(LookupError):
    """No such method in this API definition."""


def methods(version: "_ty.Mapping[str, _ty.Any]") -> "dict[str, dict]":
    """``{name: method}`` for one dump version entry."""
    return {m["name"]: m for m in version.get("methods") or []}


def namespaces(names: "_ty.Iterable[str]") -> "dict[str, int]":
    """``{namespace: method count}``, where a namespace is everything but the
    last dotted segment (``pool.dataset.query`` -> ``pool.dataset``)."""
    counts: "dict[str, int]" = {}
    for name in names:
        namespace = name.rpartition(".")[0] or name
        counts[namespace] = counts.get(namespace, 0) + 1
    return dict(sorted(counts.items()))


def find(version: "_ty.Mapping[str, _ty.Any]", name: str) -> dict:
    """The method entry for ``name``, or :class:`UnknownMethod` with near-misses."""
    found = methods(version)
    if name in found:
        return found[name]
    import difflib

    close = difflib.get_close_matches(name, found, n=5)
    hint = f"; did you mean: {', '.join(close)}" if close else ""
    raise UnknownMethod(f"no method named {name!r}{hint}")


# -- schema -> human text ---------------------------------------------------


def _enum_values(schema: "_ty.Mapping[str, _ty.Any]") -> "list | None":
    if "const" in schema:
        return [schema["const"]]
    if schema.get("enum"):
        return list(schema["enum"])
    return None


def type_label(schema: "_ty.Any") -> str:
    """A short human type for one schema (``string``, ``integer|null``, ...).

    Mirrors what the stub generator decides, in prose rather than Python: a
    list ``type`` is a union, ``anyOf``/``oneOf`` are unions of their members,
    and an array says what it holds. Deliberately total -- an unrecognized
    shape reads ``any`` instead of raising, because help that fails is worse
    than help that is vague.
    """
    if isinstance(schema, str):
        return schema
    if not isinstance(schema, _ty.cast(type, dict)):
        return "any"

    for key in ("anyOf", "oneOf"):
        members = schema.get(key)
        if members:
            seen = []
            for member in members:
                label = type_label(member)
                if label not in seen:
                    seen.append(label)
            return "|".join(seen)
    if schema.get("allOf") and len(schema["allOf"]) == 1:
        return type_label(schema["allOf"][0])

    declared = schema.get("type")
    if isinstance(declared, (list, tuple)):
        seen = []
        for member in declared:
            label = type_label({**schema, "type": member})
            if label not in seen:
                seen.append(label)
        return "|".join(seen)
    if declared == "array":
        items = schema.get("items")
        if isinstance(items, dict) and items:
            return f"array[{type_label(items)}]"
        return "array"
    if declared == "object":
        extra = schema.get("additionalProperties")
        if isinstance(extra, dict) and extra and not schema.get("properties"):
            return f"object[str, {type_label(extra)}]"
        return "object"
    if isinstance(declared, str):
        return declared.removeprefix("!")
    return "any"


_MISSING = object()


def _default_text(schema: "_ty.Mapping[str, _ty.Any]") -> "str | None":
    import json

    value = schema.get("default", _MISSING)
    if value is _MISSING:
        return None
    try:
        return json.dumps(value)
    except (TypeError, ValueError):
        return repr(value)


def _describe(schema: "_ty.Mapping[str, _ty.Any]") -> str:
    text = schema.get("description") or ""
    return " ".join(str(text).split())


def _properties(schema: "_ty.Any") -> "dict[str, dict] | None":
    """The properties of an object schema, looking through a single-member
    union -- the dump writes an optional payload as ``anyOf[object, null]``."""
    if not isinstance(schema, dict):
        return None
    if schema.get("properties"):
        return schema["properties"]
    for key in ("anyOf", "oneOf"):
        for member in schema.get(key) or []:
            if isinstance(member, dict) and member.get("properties"):
                return member["properties"]
    return None


def _required(schema: "_ty.Any") -> "set[str]":
    if not isinstance(schema, dict):
        return set()
    if schema.get("properties"):
        return set(schema.get("required") or [])
    for key in ("anyOf", "oneOf"):
        for member in schema.get(key) or []:
            if isinstance(member, dict) and member.get("properties"):
                return set(member.get("required") or [])
    return set()


def parameters(method: "_ty.Mapping[str, _ty.Any]") -> "list[dict]":
    """The positional parameter schemas, in order."""
    schemas = method.get("schemas") or {}
    props = schemas.get("properties") or {}
    call = props.get(_CALL_PARAMS) or {}
    return list(call.get("prefixItems") or [])


def returns(method: "_ty.Mapping[str, _ty.Any]") -> "dict":
    schemas = method.get("schemas") or {}
    return (schemas.get("properties") or {}).get(_RETURN) or {}


def payload_index(method: "_ty.Mapping[str, _ty.Any]") -> "int | None":
    """Index of the parameter that ``--field=value`` fills.

    The **last** object-typed parameter: ``user.create(payload)`` has one, and
    ``user.update(id, payload)`` puts it second, so the earlier positionals stay
    with ``-p`` where they belong.
    """
    found = None
    for index, schema in enumerate(parameters(method)):
        if _properties(schema) is not None:
            found = index
    return found


def fields(method: "_ty.Mapping[str, _ty.Any]") -> "dict[str, dict]":
    """The ``--field=value`` names for this method, ``{}`` when it takes none."""
    index = payload_index(method)
    if index is None:
        return {}
    return _properties(parameters(method)[index]) or {}


# -- rendering ---------------------------------------------------------------


def usage(name: str, method: "_ty.Mapping[str, _ty.Any]") -> str:
    """The one-line usage, in the syntax the ``call`` command accepts."""
    params = parameters(method)
    payload = payload_index(method)
    parts = ["pytruenas call", name]
    for index, schema in enumerate(params):
        if index == payload:
            continue
        label = schema.get("title") or f"arg{index + 1}"
        parts.append(f"-p <{' '.join(str(label).split())}>")
    parts.append("<target>")
    if payload is not None:
        parts.append("-- --field=value ...")
    return " ".join(parts)


def _field_lines(
    name: str, schema: "_ty.Mapping[str, _ty.Any]", required: bool
) -> "list[str]":
    bits = ["required"] if required else []
    default = _default_text(schema)
    if default is not None:
        bits.append(f"default {default}")
    head = f"  --{name}=<{type_label(schema)}>"
    lines = [f"{head:<40}{('(' + ', '.join(bits) + ')') if bits else ''}".rstrip()]
    values = _enum_values(schema)
    if values:
        rendered = ", ".join(repr(v) for v in values)
        lines += _textwrap.wrap(
            f"one of: {rendered}",
            WIDTH,
            initial_indent=" " * 6,
            subsequent_indent=" " * 14,
        )
    described = _describe(schema)
    if described:
        lines += _textwrap.wrap(
            described, WIDTH, initial_indent=" " * 6, subsequent_indent=" " * 6
        )
    return lines


def render(name: str, method: "_ty.Mapping[str, _ty.Any]") -> str:
    """Full help for one method."""
    out: "list[str]" = [usage(name, method), ""]

    doc = " ".join(str(method.get("doc") or "").split())
    if doc:
        out += _textwrap.wrap(doc, WIDTH)
        out.append("")

    roles = method.get("roles") or []
    if roles:
        out.append(f"Roles: {', '.join(str(r) for r in roles)}")
        out.append("")

    params = parameters(method)
    payload = payload_index(method)
    positional = [(i, s) for i, s in enumerate(params) if i != payload]
    if positional:
        out.append("Positional parameters (-p, JSON):")
        for index, schema in positional:
            title = " ".join(str(schema.get("title") or f"arg{index + 1}").split())
            bits = [type_label(schema)]
            default = _default_text(schema)
            bits.append(f"default {default}" if default is not None else "required")
            out.append(f"  -p <{title}>".ljust(34) + f"({', '.join(bits)})")
            described = _describe(schema)
            if described:
                out += _textwrap.wrap(
                    described, WIDTH, initial_indent=" " * 6, subsequent_indent=" " * 6
                )
        out.append("")

    if payload is not None:
        props = fields(method)
        required = _required(params[payload])
        out.append("Fields (after --):" if props else "Fields: none")
        for field, schema in props.items():
            out += _field_lines(field, schema, field in required)
        out.append("")

    result = returns(method)
    out.append(f"Returns: {type_label(result)}")
    described = _describe(result)
    if described:
        out += _textwrap.wrap(
            described, WIDTH, initial_indent=" " * 2, subsequent_indent=" " * 2
        )
    return "\n".join(out).rstrip() + "\n"


def render_namespace(version: "_ty.Mapping[str, _ty.Any]", namespace: str) -> str:
    """List the methods of one namespace with their first doc line."""
    found = methods(version)
    prefix = namespace + "."
    selected = {n: m for n, m in found.items() if n.startswith(prefix)}
    if not selected:
        raise UnknownMethod(f"no methods in namespace {namespace!r}")
    out = [f"{namespace} -- {len(selected)} method(s)", ""]
    width = max(len(n) for n in selected) - len(namespace) - 1
    for name in sorted(selected):
        doc = " ".join(str(selected[name].get("doc") or "").split())
        first = doc.split(". ")[0][: WIDTH - width - 6]
        out.append(f"  {name[len(prefix):]:<{width}}  {first}".rstrip())
    return "\n".join(out) + "\n"


def render_index(version: "_ty.Mapping[str, _ty.Any]") -> str:
    """List every namespace with its method count."""
    counts = namespaces(methods(version))
    out = [
        f"{len(methods(version))} methods in {len(counts)} namespaces "
        f"(API {version.get('version', '?')})",
        "",
    ]
    width = max((len(n) for n in counts), default=1)
    for namespace, count in counts.items():
        out.append(f"  {namespace:<{width}}  {count}")
    out.append("")
    out.append(
        "Try: pytruenas help <namespace>   or   pytruenas help <namespace>.<method>"
    )
    return "\n".join(out) + "\n"
