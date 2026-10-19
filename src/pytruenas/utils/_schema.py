"""Read a method entry of a middleware API definition.

One reading for the typings generator, ``help`` and ``call --field``. A method
keeps its positional parameters in ``schemas.properties["Call parameters"]``
as ``prefixItems`` and its result in ``["Return value"]``. Every function is
pure and tolerant: a missing key reads as empty rather than raising.
"""

from __future__ import annotations

import re as _re
import typing as _ty

CALL_PARAMS = "Call parameters"
RETURN = "Return value"


def parameters(method: "_ty.Mapping[str, _ty.Any]") -> "list[_ty.Any]":
    """The positional parameter schemas, in order."""
    schemas = method.get("schemas") or {}
    call = (schemas.get("properties") or {}).get(CALL_PARAMS) or {}
    return list(call.get("prefixItems") or [])


def returns(method: "_ty.Mapping[str, _ty.Any]") -> "_ty.Any":
    """The return value's schema, ``{}`` when the method declares none."""
    schemas = method.get("schemas") or {}
    return (schemas.get("properties") or {}).get(RETURN) or {}


def object_member(schema: "_ty.Any") -> "dict | None":
    """The object schema that carries ``properties``: ``schema`` itself, or the
    first ``anyOf``/``oneOf`` member that has them (the dump writes an optional
    payload as ``anyOf[object, null]``). ``None`` when there is none."""
    if not isinstance(schema, dict):
        return None
    if schema.get("properties"):
        return schema
    for key in ("anyOf", "oneOf"):
        for member in schema.get(key) or []:
            if isinstance(member, dict) and member.get("properties"):
                return member
    return None


def properties(schema: "_ty.Any") -> "dict[str, _ty.Any] | None":
    """The properties of an object schema, looking through a union."""
    found = object_member(schema)
    return None if found is None else found["properties"]


def required(schema: "_ty.Any") -> "set[str]":
    """The required property names of an object schema, looking through a union."""
    found = object_member(schema)
    return set() if found is None else set(found.get("required") or [])


def payload_index(method: "_ty.Mapping[str, _ty.Any]") -> "int | None":
    """Index of the payload: the **last** parameter that is an object with
    properties (``user.update(id, payload)`` puts it second), or ``None``."""
    found = None
    for index, schema in enumerate(parameters(method)):
        if object_member(schema) is not None:
            found = index
    return found


def enum_values(schema: "_ty.Mapping[str, _ty.Any]") -> "list | None":
    """The values a ``const``/``enum`` schema allows, or ``None``."""
    if "const" in schema:
        return [schema["const"]]
    if schema.get("enum"):
        return list(schema["enum"])
    return None


def unwrap_optional(schema: "_ty.Any") -> "dict":
    """Collapse a union to the member that carries the shape.

    ``anyOf: [<real>, {"type": "null"}]`` becomes ``<real>`` with ``"null"``
    added to its ``type``. A union of several real shapes keeps only the list
    of their types.
    """
    if not isinstance(schema, dict):
        return {}
    for key in ("anyOf", "oneOf"):
        members = [m for m in (schema.get(key) or []) if isinstance(m, dict)]
        if not members:
            continue
        real = [m for m in members if m.get("type") != "null"]
        nullable = len(real) != len(members)
        if len(real) == 1:
            merged = dict(real[0])
            if nullable:
                declared = merged.get("type")
                if isinstance(declared, str):
                    merged["type"] = [declared, "null"]
                elif isinstance(declared, (list, tuple)):
                    merged["type"] = [*declared, "null"]
            return merged
        return {"type": [*(m.get("type") for m in members)]}
    return dict(schema)


def words(name: str) -> "list[str]":
    """The words of a dump name: every non-alphanumeric character, underscore
    included, separates two (titles hold spaces, dashes, parens and colons)."""
    return [part for part in _re.split(r"[^0-9A-Za-z]+", name) if part]
