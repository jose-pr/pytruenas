from __future__ import annotations

import re as _re
import typing as _ty
from duho import qualname as _qn

JsonNumber = _ty.Union[float, int]
# Real aliases, not strings: a stub annotation naming `_jsonschema.JsonValue`
# used to resolve to a `str` VARIABLE, which is not a type at all. Written with
# `_ty.Any` at the leaves because a recursive alias needs 3.12 to be expressed
# directly, and the stubs must resolve on the 3.9 floor.
JsonValue = _ty.Union[
    str, int, float, bool, None, _ty.Sequence[_ty.Any], _ty.Mapping[str, _ty.Any]
]
JsonObject = _ty.Mapping[str, JsonValue]
JsonArray = _ty.Sequence[JsonValue]


def _typeddict_name(namespace: "_qn.PythonName", title: str) -> str:
    """Build a valid CamelCase TypedDict name from ``namespace`` + ``title``.

    ``title`` may contain spaces/dashes/dots (real dumps have titles like
    ``"Filesystem Count"`` or ``"query-options"``); those all become word
    boundaries, and empty parts are dropped (so a ``pysafe`` trailing ``_`` does
    not crash camelcasing -- see the ``duho.text.camelcase`` trailing-separator
    bug). The namespace prefix keeps names unique across sibling namespaces.
    """
    raw = "/".join([*namespace.parts, title])
    parts = []
    # Split on every non-alphanumeric character (underscore included, which
    # `\W` would keep), not only . _ - /: a title like
    # "acl(nfs4)" or "smb:share" otherwise produced a name no stub can define.
    for chunk in _re.split(r"[^0-9A-Za-z]+", raw):
        if chunk:
            parts.append(chunk[:1].upper() + chunk[1:])
    name = "".join(parts) or "Anon"
    # Ensure a valid identifier start (a title beginning with a digit, etc.).
    if not (name[0].isalpha() or name[0] == "_"):
        name = "_" + name
    return name


class Schema(_ty.TypedDict, total=False):
    title: _ty.NotRequired[str]
    description: _ty.NotRequired[str]
    default: _ty.NotRequired[object | None]

    def get_type(schema) -> "type[AnyOf|BaseType|OneOf]":  # type: ignore
        if "anyOf" in schema:
            return AnyOf
        elif "oneOf" in schema:
            return OneOf
        else:
            return BaseType

    def python_declaration(
        self, typeddicts: dict[str, object], namespace: _qn.PythonName
    ):
        if isinstance(self, str):
            self = _ty.cast(Schema, {"type": self})
        return Schema.get_type(self).python_declaration(
            self,  # type: ignore
            typeddicts,
            namespace,
        )


class BaseType(Schema):
    type: _ty.NotRequired[str]

    def python_declaration(
        self, typeddicts: dict[str, object], namespace: _qn.PythonName
    ):
        type = self.get("type", "any")
        if isinstance(type, str) and type.startswith("!"):
            return type.removeprefix("!")
        if isinstance(type, (list, tuple)):
            # A list of types is a union of them (JSON Schema allows it, and the
            # middleware dump uses it); this used to raise NotImplementedError
            # and abort the whole generation.
            members = []
            for member in type:
                rendered = BaseType.python_declaration(
                    _ty.cast(_ty.Any, {**self, "type": member}), typeddicts, namespace
                )
                if rendered not in members:
                    members.append(rendered)
            return "|".join(members) if members else "_jsonschema.JsonValue"
        for ty in TYPES:
            if ty.type == type:  # type: ignore
                return ty.python_declaration(self, typeddicts, namespace)
        # An unknown type name is imprecise, not fatal: the stub says "some
        # JSON value" rather than failing to generate at all.
        return "_jsonschema.JsonValue"

        ...


#: `typing.Never` is 3.11+; the stubs must resolve on the 3.9 floor.
_HAS_NEVER = hasattr(_ty, "Never")

TypeDeclaration = _ty.Union[BaseType, str]


class AnyOf(Schema):
    anyOf: list[TypeDeclaration]

    def python_declaration(
        self, typeddicts: dict[str, object], namespace: _qn.PythonName
    ):  # type: ignore
        return "|".join(
            [
                Schema.python_declaration(_ty.cast(Schema, t), typeddicts, namespace)
                for t in self["anyOf"]
            ]
        )


class OneOf(Schema):
    oneOf: list[TypeDeclaration]

    def python_declaration(
        self, typeddicts: dict[str, object], namespace: _qn.PythonName
    ):  # type: ignore
        return "|".join(
            [
                Schema.python_declaration(_ty.cast(Schema, t), typeddicts, namespace)
                for t in self["oneOf"]
            ]
        )


class Float(BaseType):
    type: _ty.Literal["float"] = "float"  # type: ignore

    def python_declaration(
        self, typeddicts: dict[str, object], namespace: _qn.PythonName
    ):  # type: ignore
        return "float"


class Null(BaseType):
    type: _ty.Literal["null"] = "null"  # type: ignore

    def python_declaration(
        self, typeddicts: dict[str, object], namespace: _qn.PythonName
    ):  # type: ignore
        return "None"


class Boolean(BaseType):
    type: _ty.Literal["boolean"] = "boolean"  # type: ignore

    def python_declaration(
        self, typeddicts: dict[str, object], namespace: _qn.PythonName
    ):  # type: ignore
        return "bool"


class Integer(BaseType):
    type: _ty.Literal["integer"] = "integer"  # type: ignore

    def python_declaration(
        self, typeddicts: dict[str, object], namespace: _qn.PythonName
    ):  # type: ignore
        return "int"


class Number(BaseType):
    type: _ty.Literal["number"] = "number"  # type: ignore

    def python_declaration(
        self, typeddicts: dict[str, object], namespace: _qn.PythonName
    ):  # type: ignore
        return "_jsonschema.JsonNumber"


class String(BaseType):
    type: _ty.Literal["string"] = "string"  # type: ignore

    def python_declaration(
        self, typeddicts: dict[str, object], namespace: _qn.PythonName
    ):  # type: ignore
        return "str"


class Object(BaseType):
    type: _ty.Literal["object"] = "object"  # type: ignore
    properties: dict[str, Schema]
    additional_properties: _ty.NotRequired[bool]
    required: _ty.NotRequired[list[str]]

    def python_declaration(
        self, typeddicts: dict[str, object], namespace: _qn.PythonName
    ):  # type: ignore
        properties = self.get("properties")
        if not properties:
            return "_jsonschema.JsonObject"

        # Absent (or empty) `required` means NOTHING is required -- JSON
        # Schema's own rule. Reading a missing list as "all required" made
        # every update payload and query-options TypedDict demand every key.
        required = self.get("required") or []
        title = self.get("_name", self.get("title"))
        if not title:
            # An anonymous inline object with properties: derive a stable name
            # from the property set so codegen never crashes on a missing title.
            title = "obj_" + "_".join(sorted(properties)[:3])
        name = _typeddict_name(namespace, title)

        typedict = {}
        for prop, defintion in properties.items():
            typedef = Schema.python_declaration(defintion, typeddicts, namespace)
            if prop not in required:
                typedef = f"_NotRequired[{typedef}]"
            typedict[prop] = typedef

        existing = typeddicts.get(name)
        if existing is not None and existing != typedict:
            # Two different shapes wanted the same name (two namespaces with
            # the same title, or a title that sanitizes to an existing name).
            # The later one used to overwrite the earlier, leaving every
            # reference to the first pointing at the wrong shape.
            suffix = 2
            while typeddicts.get(f"{name}{suffix}") not in (None, typedict):
                suffix += 1
            name = f"{name}{suffix}"
        typeddicts[name] = typedict

        return name


class Any(BaseType):
    type: _ty.Literal["any"] = "any"  # type: ignore

    def python_declaration(
        self, typeddicts: dict[str, object], namespace: _qn.PythonName
    ):  # type: ignore
        return "_jsonschema.JsonValue"


class Array(BaseType):
    type: _ty.Literal["array"] = "array"  # type: ignore
    items: Schema | bool
    prefixItems: list[Schema]

    def python_declaration(
        self, typeddicts: dict[str, object], namespace: _qn.PythonName
    ):  # type: ignore
        items = self.get("items")
        if items is True or items == {}:
            # "any item is allowed" -- a list of anything.
            return "_jsonschema.JsonArray"
        if items is False:
            # Nothing may appear in the array; the only valid value is empty.
            return "list[_ty.Never]" if _HAS_NEVER else "list"
        if not items:
            return "_jsonschema.JsonArray"
        return f"list[{Schema.python_declaration(items, typeddicts, namespace)}]"


TYPES: list[type[BaseType]] = [
    Float,
    Null,
    Boolean,
    Integer,
    String,
    Object,
    Array,
    Any,
    Number,
]  # type: ignore
# name: str
# title: str #type: ignore
# required: bool
# type: "str|list[str|Parameter]"
# description: str
# items: 'list[Parameter]'
# properties: 'dict[str,Parameter]'
