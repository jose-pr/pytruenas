import typing as _ty

JsonNumber: _ty.TypeAlias = float | int
JsonValue: _ty.TypeAlias = "str|int|float|bool|None|JsonArray|JsonObject"
JsonObject: _ty.TypeAlias = "dict[str, JsonValue]"
JsonArray: _ty.TypeAlias = "list[JsonValue]"


class Schema(_ty.TypedDict):
    title: _ty.NotRequired[str]
    description: _ty.NotRequired[str]
    default: _ty.NotRequired[object | None]

    def get_type(schema) -> "type[AnyOf|BaseType|OneOf]":  # type:ignore
        if "anyOf" in schema:
            return AnyOf
        elif "oneOf" in schema:
            return OneOf
        else:
            return BaseType

    def python_declaration(schema, typeddicts: dict[str, object]):  # type:ignore
        if isinstance(schema, str):
            schema = _ty.cast(Schema, {"type": schema})
        return Schema.get_type(schema).python_declaration(
            schema, typeddicts  # type:ignore
        )


class BaseType(Schema):
    type: _ty.NotRequired[str]

    def python_declaration(self, typeddicts: dict[str, object]):  # type:ignore
        type = self.get("type", "any")
        if isinstance(type, str) and type.startswith("!"):
            return type.removeprefix("!")
        for ty in TYPES:
            if ty.type == type:  # type:ignore
                return ty.python_declaration(self, typeddicts)
        raise NotImplementedError(type)

        ...


TypeDeclaration: _ty.TypeAlias = BaseType | str


class AnyOf(Schema):
    anyOf: list[TypeDeclaration]

    def python_declaration(self, typeddicts: dict[str, object]):  # type:ignore
        return "|".join(
            [
                Schema.python_declaration(_ty.cast(Schema, t), typeddicts)
                for t in self["anyOf"]
            ]
        )


class OneOf(Schema):
    oneOf: list[TypeDeclaration]

    def python_declaration(self, typeddicts: dict[str, object]):  # type:ignore
        return "|".join(
            [
                Schema.python_declaration(_ty.cast(Schema, t), typeddicts)
                for t in self["oneOf"]
            ]
        )


class Float(BaseType):
    type: _ty.Literal["float"] = "float"  # type:ignore

    def python_declaration(self, typeddicts: dict[str, object]):  # type:ignore
        return "float"


class Null(BaseType):
    type: _ty.Literal["null"] = "null"  # type:ignore

    def python_declaration(self, typeddicts: dict[str, object]):  # type:ignore
        return "None"


class Boolean(BaseType):
    type: _ty.Literal["boolean"] = "boolean"  # type:ignore

    def python_declaration(self, typeddicts: dict[str, object]):  # type:ignore
        return "bool"


class Integer(BaseType):
    type: _ty.Literal["integer"] = "integer"  # type:ignore

    def python_declaration(self, typeddicts: dict[str, object]):  # type:ignore
        return "int"


class Number(BaseType):
    type: _ty.Literal["number"] = "number"  # type:ignore

    def python_declaration(self, typeddicts: dict[str, object]):  # type:ignore
        return "_jsonschema.JsonNumber"


class String(BaseType):
    type: _ty.Literal["string"] = "string"  # type:ignore

    def python_declaration(self, typeddicts: dict[str, object]):  # type:ignore
        return "str"


class Object(BaseType):
    type: _ty.Literal["object"] = "object"  # type:ignore
    properties: dict[str, Schema]
    additional_properties: bool
    required: _ty.NotRequired[list[str]]

    def python_declaration(self, typeddicts: dict[str, object]):  # type:ignore
        properties = self.get("properties")
        if not properties:
            return "_jsonschema.JsonObject"

        required = self.get("required", [])
        extras = self.get("additional_properties", None)
        name = self["title"]  # type:ignore
        if extras:
            pass
        typedict = {}
        for prop, defintion in properties.items():
            typedef = Schema.python_declaration(defintion, typeddicts)
            if prop not in required:
                typedef = f"_ty.NotRequired[{typedef}]"
            default = defintion.get("default", ...)
            if default != ...:
                pass

            typedict[prop] = typedef

        typeddicts[name] = typedict

        return name


class Any(BaseType):
    type: _ty.Literal["any"] = "any"  # type:ignore

    def python_declaration(self, typeddicts: dict[str, object]):  # type:ignore
        return "_jsonschema.JsonValue"


class Array(BaseType):
    type: _ty.Literal["array"] = "array"  # type:ignore
    items: Schema

    def python_declaration(self, typeddicts: dict[str, object]):  # type:ignore
        items = self["items"]
        if not items:
            return "_jsonschema.JsonArray"
        return f"list[{Schema.python_declaration(items, typeddicts)}]"


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
]  # type:ignore
# name: str
# title: str #type: ignore
# required: bool
# type: "str|list[str|Parameter]"
# description: str
# items: 'list[Parameter]'
# properties: 'dict[str,Parameter]'
