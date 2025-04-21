import typing as _ty


class Schema(_ty.TypedDict):
    type: str
    title: _ty.NotRequired[str]

class Object(Schema):
    type: _ty.Literal["object"]
    properties: dict[str, Schema]
    required: _ty.NotRequired[list[str]]


class Array(Schema):
    type: _ty.Literal["array"]
    prefixItems: list[Schema]
    items: bool
