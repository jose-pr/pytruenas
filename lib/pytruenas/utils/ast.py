import ast as _ast
import inspect as _inspect
import sys as _sys
import typing as _ty
from dataclasses import dataclass as _data
from pathlib import Path as _Path


def getclsdef(cls: type):
    try:
        src = _inspect.getsource(cls)
    except OSError:
        pass

        file: str | None = getattr(cls, "__file__", None)
        if not file:
            module = getattr(cls, "__module__")
            module = _sys.modules[module]
            file = getattr(module, "__file__", None)

        if not file:
            raise OSError("No source avalible")

        src = _Path(file).read_text()

    for node in _ast.walk(_ast.parse(src)):
        if isinstance(node, _ast.ClassDef) and node.name == cls.__name__:
            return node

    raise OSError("Class Definition Not Found")


class NotDefined: ...


NOT_DEFINED = NotDefined()


@_data
class ArgDeclaration:
    default: object
    type: type
    annotations: list
    docstring: str
    exprs: list


def get_clsargs(cls: type):
    typehints = _ty.get_type_hints(cls, include_extras=True)
    constants = get_clsargs_constants(cls)
    args: dict[str, ArgDeclaration] = {}
    for name, type in typehints.items():
        annotations = []
        if hasattr(type, "__metadata__"):
            annotations.extend(type.__metadata__)
            type = type.__origin__

        argcontant = constants.get(name, [])
        if argcontant and isinstance(argcontant[0], str):
            docstring = argcontant[0]
            argcontant = argcontant[1:]
        else:
            docstring = ""
        args[name] = ArgDeclaration(
            type=type,
            default=getattr(cls, name, NOT_DEFINED),
            annotations=annotations,
            docstring=docstring,
            exprs=argcontant,
        )

    return args


def get_clsargs_constants(cls: type):
    argsexprs: dict[str, list] = {}
    bases = [cls]
    while bases:
        for base in bases:
            try:
                clsdef = getclsdef(base)
            except TypeError:
                continue
            argument = None
            for node in clsdef.body:
                if isinstance(node, (_ast.Assign, _ast.AnnAssign)):
                    if hasattr(node, "targets"):
                        target = node.targets[0]  # type:ignore
                    else:
                        target = node.target  # type:ignore
                    if not isinstance(target, _ast.Name):
                        argument = None
                    else:
                        argument = target.id
                    continue
                elif isinstance(node, _ast.Expr) and argument:
                    props = argsexprs.setdefault(argument, [])
                    props.append(_ast.literal_eval(node.value))
                else:
                    argument = None

        bases = base.__bases__  # type:ignore

    return argsexprs
