"""A schema from the API definition as a Python type expression in a stub.

The expressions name the stub module's own imports: ``_ty`` (``typing``),
``_jsonschema`` (:mod:`pytruenas.models.jsonschema`) and ``_NotRequired``.
An object with properties becomes a TypedDict, collected into ``typeddicts``
(``{name: {key: type expression}}``) for the module to define.
"""

from __future__ import annotations

import re as _re
import typing as _ty

from duho import qualname as _qn

#: `typing.Never` is 3.11+; the stubs must resolve on the 3.9 floor.
_HAS_NEVER = hasattr(_ty, "Never")

_SCALARS = {
    "float": "float",
    "null": "None",
    "boolean": "bool",
    "integer": "int",
    "string": "str",
    "number": "_jsonschema.JsonNumber",
    "any": "_jsonschema.JsonValue",
}


def class_name(name: str) -> str:
    """CamelCase a dump name into a class name.

    Every non-alphanumeric character, underscore included, separates two words
    and empty parts are dropped: ``global_`` (a ``pysafe`` output) becomes
    ``Global`` and ``acl(nfs4)`` ``AclNfs4``. A leading digit gets an ``N``.
    """
    parts = [part for part in _re.split(r"[^0-9A-Za-z]+", name) if part]
    result = "".join(part[:1].upper() + part[1:] for part in parts)
    if not result:
        return "Unnamed"
    return f"N{result}" if result[0].isdigit() else result


def typeddict_name(namespace: "_qn.PythonName", title: str) -> str:
    """The TypedDict name for an object titled ``title`` in ``namespace``.

    The namespace prefix keeps names unique across sibling namespaces.
    """
    return class_name("/".join([*namespace.parts, title]))


def declaration(
    schema: "_ty.Any",
    typeddicts: "dict[str, dict[str, str]]",
    namespace: "_ty.Optional[_qn.PythonName]",
) -> str:
    """The type expression for ``schema``; a bare string is a ``type`` name.

    A form this cannot express is ``_jsonschema.JsonValue``, never an error.
    """
    if isinstance(schema, str):
        schema = {"type": schema}
    for key in ("anyOf", "oneOf"):
        if key in schema:
            return "|".join(
                declaration(member, typeddicts, namespace) for member in schema[key]
            )
    return _typed(schema, typeddicts, namespace)


def _typed(schema, typeddicts, namespace) -> str:
    # `enum`/`const` say more than `type` does, and the appliance's dump is
    # full of them (6413 and 6420 occurrences on 26.0).
    literal = _literal(schema)
    if literal is not None:
        return literal
    if "allOf" in schema:
        members = [
            declaration(member, typeddicts, namespace)
            for member in schema.get("allOf") or []
        ]
        # One member is just that member; several would need a real
        # intersection type, which Python has no syntax for.
        if len(members) == 1:
            return members[0]
    type_ = schema.get("type", "any")
    if isinstance(type_, str) and type_.startswith("!"):
        # Already a type expression: what the synthetic helpers write.
        return type_[1:]
    if isinstance(type_, (list, tuple)):
        # A list of types is a union of them.
        members = []
        for member in type_:
            rendered = _typed({**schema, "type": member}, typeddicts, namespace)
            if rendered not in members:
                members.append(rendered)
        return "|".join(members) if members else "_jsonschema.JsonValue"
    if type_ == "object":
        return _object(schema, typeddicts, namespace)
    if type_ == "array":
        return _array(schema, typeddicts, namespace)
    if isinstance(type_, str) and type_ in _SCALARS:
        return _SCALARS[type_]
    return "_jsonschema.JsonValue"


def _literal(schema: "_ty.Mapping[str, object]") -> "_ty.Optional[str]":
    """``Literal[...]`` for a ``const``/``enum`` schema, or ``None``.

    ``None`` among the values becomes a union member rather than a Literal
    argument. A value no Literal can carry -- a list, a dict, a float -- falls
    back to the ordinary ``type`` handling.
    """
    if "const" in schema:
        values = [schema["const"]]
    elif "enum" in schema:
        values = list(schema.get("enum") or [])
        if not values:
            return None
    else:
        return None
    literals = []
    optional = False
    for value in values:
        if value is None:
            optional = True
        elif isinstance(value, (bool, str, int)):
            literals.append(repr(value))
        else:
            return None
    if not literals:
        return "None" if optional else None
    rendered = f"_ty.Literal[{', '.join(literals)}]"
    return f"{rendered}|None" if optional else rendered


def _object(schema, typeddicts, namespace) -> str:
    properties = schema.get("properties")
    if not properties:
        extra = schema.get("additionalProperties")
        if isinstance(extra, dict) and extra:
            # A map whose VALUES have a schema (19309 occurrences on 26.0).
            value = declaration(extra, typeddicts, namespace)
            return f"_ty.Mapping[str, {value}]"
        return "_jsonschema.JsonObject"

    # Absent (or empty) `required` means NOTHING is required: JSON Schema's
    # own rule.
    required = schema.get("required") or []
    title = schema.get("_name", schema.get("title"))
    if not title:
        # An anonymous object: a stable name from its property set.
        title = "obj_" + "_".join(sorted(properties)[:3])
    name = typeddict_name(namespace, title)

    keys = {}
    for key, member in properties.items():
        typedef = declaration(member, typeddicts, namespace)
        if key not in required:
            typedef = f"_NotRequired[{typedef}]"
        keys[key] = typedef

    existing = typeddicts.get(name)
    if existing is not None and existing != keys:
        # Two different shapes want one name: number the later one, so no
        # reference to the first ends up naming the wrong shape.
        suffix = 2
        while typeddicts.get(f"{name}{suffix}") not in (None, keys):
            suffix += 1
        name = f"{name}{suffix}"
    typeddicts[name] = keys
    return name


def _array(schema, typeddicts, namespace) -> str:
    items = schema.get("items")
    if items is True or items == {}:
        return "_jsonschema.JsonArray"
    if items is False:
        # Nothing may appear in the array; the only valid value is empty.
        return "list[_ty.Never]" if _HAS_NEVER else "list"
    if not items:
        return "_jsonschema.JsonArray"
    return f"list[{declaration(items, typeddicts, namespace)}]"
