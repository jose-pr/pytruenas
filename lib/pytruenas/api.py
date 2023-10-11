from dataclasses import dataclass as _dataclass, field as _field
import json
import typing as _ty
import re as _re
from . import _core, _utils

_FORWARDREF = _re.compile(r"ForwardRef\('([^']*)'\)")


@_dataclass
class Type:
    _src: dict = _field(init=False, repr=False)

    def python(self) -> "type | Object":
        py = self._python()
        ty = str(py)
        if "<" in ty:
            ty = py.__name__
        ty = _FORWARDREF.sub(r"\1", ty)
        return ty.replace("'", "")

    def _python(self):
        raise NotImplementedError(self)

    def required_types(self) -> "_ty.Generator[Type]":
        yield self
        yield from self._required_types()

    def _required_types(self) -> "_ty.Generator[Type]":
        yield from []

    def from_openapi(src: _core.Parameter | str):
        if isinstance(src, Type):
            return src
        src: _core.Parameter = src if isinstance(src, dict) else {"type": src}
        if isinstance(src.get("type", None), list):
            src = {"oneOf": src["type"]}
        if "anyOf" in src:
            ty = AnyOf(types=[Type.from_openapi(t) for t in src["anyOf"]])
        elif "oneOf" in src:
            ty = OneOf(types=[Type.from_openapi(t) for t in src["oneOf"]])
        elif "type" not in src:
            ty = ValueError(src)
        else:
            match src["type"]:
                case "float":
                    ty = Float()
                case "null":
                    ty = Null()
                case "boolean":
                    ty = Boolean()
                case "integer":
                    ty = Integer()
                case "string":
                    ty = String()
                case "array":
                    item = src.get("items", [])
                    if item:
                        ty = Array(Type.from_openapi(item[0]))
                    else:
                        ty = Array(entry_type=None)
                case "object":
                    if "properties" not in src:
                        ty = Object(
                            name=src.get("_name_", "Object"),
                            properties=_ty.OrderedDict(),
                        )
                    else:
                        ty = Object(
                            src.get("_name_", "Object"),
                            _ty.OrderedDict(
                                [
                                    (name, Type.from_openapi(prop))
                                    for name, prop in src["properties"].items()
                                ]
                            ),
                        )
                case _other:
                    raise ValueError(_other)

        ty._src = src
        if "enum" in src:
            options = [*src["enum"]]
            def _getopts(ty: Type):
                
                if isinstance(ty, (AnyOf, OneOf)):
                    _basety = None
                    for t in ty.types:
                         t = _getopts(t)
                         if not _basety:
                             _basety = t
                    return _basety
                elif isinstance(ty, Enum):
                    _basety = _getopts(ty.type)
                    for opt in ty.options:
                        if opt not in options:
                            options.append(opt)
                    return _basety
                else:
                    return ty

            _basety = _getopts(ty)
            _basety._src = src
            ty = Enum(name=src.get("_name_", "Choices"), type=_basety, options=options)

        return ty


@_dataclass
class AnyOf(Type):
    types: list[Type]

    def _python(self):
        return _ty.Union[tuple([t._python() for t in self.types])]  # type: ignore

    def _required_types(self):
        for t in self.types:
            yield from t.required_types()


@_dataclass
class OneOf(Type):
    types: list[Type]

    def _python(self):
        return _ty.Union[tuple([t._python() for t in self.types])]  # type: ignore

    def _required_types(self):
        for t in self.types:
            yield from t.required_types()


class String(Type):
    def _python(self):
        return str


class Integer(Type):
    def _python(self):
        return int


class Float(Type):
    def _python(self):
        return float


class Null(Type):
    def _python(self):
        return None


class Boolean(Type):
    def _python(self):
        return bool


@_dataclass
class Array(Type):
    entry_type: Type

    def _python(self) -> str:
        if self.entry_type:
            return list[self.entry_type._python()]
        else:
            return list

    def _required_types(self):
        if self.entry_type:
            yield from self.entry_type.required_types()
        else:
            yield from []


@_dataclass
class Object(Type):
    name: str
    properties: _ty.OrderedDict[str, Type]

    def __bool__(self) -> int:
        return self.properties.__len__() > 0

    def __eq__(self, other):
        if not isinstance(other, Object):
            # don't attempt to compare against unrelated types
            return False
        a = self.properties
        b = other.properties
        if len(a) != len(b):
            return False
        for k, v in a.items():
            if k not in b:
                return False
            diff = _utils.diff(b[k]._src, v._src)
            diff.pop("description", None)
            if diff:
                return False
        return True

    def _python(self):
        if self.properties:
            return self.name
        else:
            return dict[str]

    def _required_types(self):
        for prop in self.properties.values():
            yield from prop.required_types()


@_dataclass
class Enum(Type):
    name: str
    type: Type
    options: list[str]

    @property
    def _src(self):
        return self.type._src

    def __bool__(self) -> int:
        return self.options.__len__() > 0

    def __eq__(self, other):
        if not isinstance(other, Enum):
            return False
        return self.options == other.options

    def _python(self):
        if len(self.options) == 1:
            return _ty.Literal[json.dumps(self.options[0])] #type:ignore
        return self.name

    def _required_types(self):
        yield from self.type.required_types()


@_dataclass
class Paramater:
    type: Type
    description: str
    default: "_ty.Any"
    required: bool

    @classmethod
    def from_param(cls, param: "_core.Parameter"):
        param = param or {}
        type = []
        desc = param.get("description", param.get("title", ""))
        required = param.get("required", True)
        type = Type.from_openapi(param)
        default = param.get("default", _utils.MISSING)
        if default is not _utils.MISSING:
            match default:
                case True:
                    ...
                case False:
                    ...
                case None:
                    ...
                case _:
                    default = json.dumps(default)
        return cls(type, desc, default, required)


@_dataclass
class MethodSignature:
    name: str
    description: str = ""
    arguments: _ty.OrderedDict[str, Paramater] = _field(
        default_factory=lambda: _ty.OrderedDict()
    )
    returns: list[Paramater] = _field(default_factory=lambda: [])
    _src: dict = None


@_dataclass
class NamespaceSignature:
    name: str
    type: str
    description: str = ""
    methods: list[MethodSignature] = _field(default_factory=lambda: [])
    _src: dict = None


@_dataclass
class Api:
    version: str
    namespaces: list[NamespaceSignature]
