import typing as _ty
from . import jsonschema as _schema


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
    properties: "MethodProperties"  # type:ignore


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
