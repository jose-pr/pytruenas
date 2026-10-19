import typing as _ty

from . import jsonschema as _schema

# The annotations MethodSchema inherits from `jsonschema.Object` are resolved
# in this module, so the names they use are bound here too.
from .jsonschema import Schema, _NotRequired  # noqa: F401


class Api(_ty.TypedDict):
    versions: "list[Version]"


class Version(_ty.TypedDict):
    version: str
    methods: "list[Method]"
    events: "list[Event]"


class Method(_ty.TypedDict):
    name: str
    roles: list[str]
    doc: str
    schemas: "MethodSchema"


class MethodSchema(_schema.Object):
    properties: "MethodProperties"  # type: ignore


MethodProperties = _ty.TypedDict(
    "MethodProperties",
    {
        "Call parameters": _schema.Array,
        "Return value": _schema.Schema,
    },
)


class Event(_ty.TypedDict):
    name: str
    roles: list[str]
    doc: str
    schemas: _schema.Schema


__all__ = [
    "Api",
    "Version",
    "Method",
    "MethodSchema",
    "MethodProperties",
    "Event",
]
