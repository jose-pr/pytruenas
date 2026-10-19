"""JSON Schema shapes, as the middleware's API definition writes them.

TypedDicts and type aliases only. Generated stubs import this module for the
``Json*`` aliases, so those names and this import path are part of every stub
tree already generated.
"""

from __future__ import annotations

import typing as _ty

JsonNumber = _ty.Union[float, int]
# Real aliases: a stub annotation names them as types. `_ty.Any` at the leaves,
# because a recursive alias needs 3.12 and the stubs resolve on the 3.9 floor.
JsonValue = _ty.Union[
    str, int, float, bool, None, _ty.Sequence[_ty.Any], _ty.Mapping[str, _ty.Any]
]
JsonObject = _ty.Mapping[str, JsonValue]
JsonArray = _ty.Sequence[JsonValue]


class Schema(_ty.TypedDict, total=False):
    title: str
    description: str
    default: _ty.Optional[object]


class BaseType(Schema, total=False):
    type: str


TypeDeclaration = _ty.Union[BaseType, str]


class AnyOf(Schema):
    anyOf: list[TypeDeclaration]


class OneOf(Schema):
    oneOf: list[TypeDeclaration]


# Each type below narrows `type` to its one value, which a checker reports as
# overwriting a TypedDict key (`[misc]`).


class Float(BaseType):
    type: _ty.Literal["float"]  # type: ignore[misc]


class Null(BaseType):
    type: _ty.Literal["null"]  # type: ignore[misc]


class Boolean(BaseType):
    type: _ty.Literal["boolean"]  # type: ignore[misc]


class Integer(BaseType):
    type: _ty.Literal["integer"]  # type: ignore[misc]


class Number(BaseType):
    type: _ty.Literal["number"]  # type: ignore[misc]


class String(BaseType):
    type: _ty.Literal["string"]  # type: ignore[misc]


class _ObjectKeys(BaseType, total=False):
    properties: dict[str, Schema]
    #: A bool ("anything"/"nothing else allowed"), or a schema the extra
    #: VALUES must match, which is how the middleware writes a map.
    additionalProperties: _ty.Union[bool, Schema]
    required: list[str]


class Object(_ObjectKeys):
    type: _ty.Literal["object"]  # type: ignore[misc]


class Any(BaseType):
    type: _ty.Literal["any"]  # type: ignore[misc]


class _ArrayKeys(BaseType, total=False):
    #: A schema every item matches, or a bool (`True`/`{}` any item, `False`
    #: none). Absent for an array with no item constraint at all.
    items: _ty.Union[Schema, bool]
    #: Positional item schemas (the middleware's call-parameter lists).
    prefixItems: list[Schema]


class Array(_ArrayKeys):
    type: _ty.Literal["array"]  # type: ignore[misc]


__all__ = [
    "JsonNumber",
    "JsonValue",
    "JsonObject",
    "JsonArray",
    "Schema",
    "BaseType",
    "TypeDeclaration",
    "AnyOf",
    "OneOf",
    "Float",
    "Null",
    "Boolean",
    "Integer",
    "Number",
    "String",
    "Object",
    "Any",
    "Array",
]
