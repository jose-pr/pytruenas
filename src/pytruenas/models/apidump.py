import typing as _ty

from . import jsonschema as _schema

# The annotations MethodSchema inherits from `jsonschema.Object` are resolved
# in this module, so the names they use are bound here too.
from .jsonschema import Schema  # noqa: F401


class API(_ty.TypedDict):
    versions: "list[Version]"


class Version(_ty.TypedDict):
    version: str
    methods: "list[APIMethod]"
    events: "list[APIEvent]"


class APIMethod(_ty.TypedDict):
    name: str
    roles: list[str]
    doc: str
    schemas: "MethodSchema"


class MethodSchema(_schema.Object):
    # Narrows the inherited `properties` key to a method's two schemas.
    properties: "MethodProperties"  # type: ignore[misc]


MethodProperties = _ty.TypedDict(
    "MethodProperties",
    {
        "Call parameters": _schema.Array,
        "Return value": _schema.Schema,
    },
)


class APIEvent(_ty.TypedDict):
    name: str
    roles: list[str]
    doc: str
    schemas: _schema.Schema


__all__ = [
    "API",
    "Version",
    "APIMethod",
    "MethodSchema",
    "MethodProperties",
    "APIEvent",
]
