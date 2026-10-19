"""Every public annotation resolves with `typing.get_type_hints`.

Run on each supported Python: a quoted `X | None` or a name imported only
under `TYPE_CHECKING` imports fine and fails here, on the oldest version
first.
"""

import importlib
import inspect
import types
import typing

import pytest

_MODULES = [
    "pytruenas.auth",
    "pytruenas.connection",
    "pytruenas.exceptions",
    "pytruenas.fs",
    "pytruenas.fs.tnasws",
    "pytruenas.host",
    "pytruenas.models.apidump",
    "pytruenas.models.jsonschema",
    "pytruenas.namespace",
    "pytruenas.providers",
    "pytruenas.utils.io",
    "pytruenas.webshell",
]

#: Dunder methods a caller writes against; other underscored names are private.
_PUBLIC_DUNDERS = {"__init__", "__call__", "__enter__"}


def _functions(cls):
    for name, member in vars(cls).items():
        if name.startswith("_") and name not in _PUBLIC_DUNDERS:
            continue
        if isinstance(member, (staticmethod, classmethod)):
            member = member.__func__
        if isinstance(member, property):
            for accessor in (member.fget, member.fset):
                if accessor is not None:
                    yield f"{cls.__name__}.{name}", accessor
        elif inspect.isfunction(member):
            yield f"{cls.__name__}.{name}", member


def _own_annotations(cls, module):
    """A class's own attribute annotations, resolved as the class body sees them."""
    own = vars(cls).get("__annotations__") or {}
    if not own:
        return None
    holder = types.FunctionType((lambda: None).__code__, vars(module))
    holder.__annotations__ = dict(own)
    return lambda: typing.get_type_hints(holder, localns=dict(vars(cls)))


def _targets():
    for module_name in _MODULES:
        module = importlib.import_module(module_name)
        for name in module.__all__:
            obj = getattr(module, name)
            if inspect.isclass(obj) and obj.__module__ == module_name:
                if hasattr(obj, "__total__") or hasattr(obj, "_fields"):
                    # TypedDict / NamedTuple: the annotations are the fields.
                    yield f"{module_name}.{name}", lambda obj=obj: (
                        typing.get_type_hints(obj)
                    )
                else:
                    check = _own_annotations(obj, module)
                    if check is not None:
                        yield f"{module_name}.{name}", check
                for label, function in _functions(obj):
                    yield f"{module_name}.{label}", lambda f=function: (
                        typing.get_type_hints(f)
                    )
            elif inspect.isfunction(obj) and obj.__module__ == module_name:
                yield f"{module_name}.{name}", lambda f=obj: typing.get_type_hints(f)


_TARGETS = dict(_targets())


@pytest.mark.parametrize("name", sorted(_TARGETS))
def test_public_annotations_resolve(name):
    _TARGETS[name]()
