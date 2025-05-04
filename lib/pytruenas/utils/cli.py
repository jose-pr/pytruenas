import argparse as _argparse
import ast as _ast
import copy as _copy
import inspect as _inspect
import pathlib as _path
import sys as _sys
import types as _types
import typing as _ty

from . import logging as _logging


class _Missing: ...


_type = type
MissingType = _type[_Missing]

_T = _ty.TypeVar("_T")

Factory = _ty.Callable[[str], _T]

NS = _argparse.Namespace
Arg = _ty.Annotated


class Argument(_ty.Protocol):
    @classmethod
    def _argbuilder_(
        cls,  # type:ignore
        name: str,
        props: "ArgAnnotations",
        default: None | object | MissingType,
        factory: Factory | None = None,
    ):
        help = props.help or ""
        flags = props.flags or ("--" + name.replace("_", "-"),)
        required = None
        cls = factory or cls  # type:ignore
        if cls is not None and cls is not Argument:
            origin = _ty.get_origin(cls)
            args = _ty.get_args(cls)
            if origin:
                if origin is _ty.Union and _types.NoneType in args:
                    args = [a for a in args if a is not _types.NoneType]
                    required = False
                    if len(args) == 1:
                        cls = args[0]
                if origin is _ty.Union or origin is _types.UnionType and len(args) > 1:

                    def cls(text: str):
                        for ty in args:
                            try:
                                return ty(text)
                            except:
                                pass
                        raise ValueError(text, args)

        return ArgumentBuilder(
            name=name,
            flags=flags,
            type=cls,
            default=default,
            help=help,
            required=required,
        )

    @classmethod
    def from_type(cls, factory: _ty.Callable[[str], _T], **kwargs):

        class Arg(cls):
            @classmethod
            def _argbuilder_(  # type:ignore
                cls,
                name: str,
                props: ArgAnnotations,
                default: None | object | MissingType,
            ):
                builder = super()._argbuilder_(name, props, default, factory)
                for k, v in kwargs.items():
                    setattr(builder, k, v)
                return builder

        return Arg


def is_argument(ty: type) -> _ty.TypeGuard[Argument]:
    builder_factory = getattr(ty, "_argbuilder_", None)
    return callable(builder_factory)


class ArgumentBuilder(_argparse.Namespace):
    name: str
    flags: list[str]
    type: Factory
    default: None | object | MissingType
    help: str
    required: bool | None = None
    action: str | _type[_argparse.Action] | None = None

    def _kwargs(self):
        kwargs = getattr(self, "kwargs", None) or {}
        if self.required is not None:
            kwargs["required"] = self.required

        if self.default is not _Missing:
            kwargs["default"] = self.default

        if self.type is bool and not self.action:
            kwargs["action"] = "store_true"
        if self.action:
            kwargs["action"] = self.action

        if kwargs.get("action") not in ["count", "store_true"]:
            kwargs["type"] = self.type

        if kwargs.get("action") == "store_true" and "default" not in kwargs:
            kwargs["default"] = False

        flags = self.flags
        dest = self.name
        if len(flags) == 1 and not flags[0].startswith("-"):
            dest = None

        if dest:
            kwargs["dest"] = dest

        return kwargs

    def add_to_parser(self, parser: _argparse.ArgumentParser):
        help = self.help
        if callable(help):  # type:ignore
            help = help()
        return parser.add_argument(
            *self.flags,
            help=help,
            **self._kwargs(),
        )


def _getclsdef(cls: type):
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

        src = _path.Path(file).read_text()

    for node in _ast.walk(_ast.parse(src)):
        if isinstance(node, _ast.ClassDef) and node.name == cls.__name__:
            return node

    raise OSError("Class Definition Not Found")


class ArgAnnotations(NS):
    help = ""
    flags = None


def _get_clsargs_props(cls):
    argsprops: dict[str, ArgAnnotations] = {}
    bases = [cls]
    while bases:
        for base in bases:
            try:
                clsdef = _getclsdef(base)
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
                    props = argsprops.setdefault(argument, ArgAnnotations())
                    if isinstance(node.value, _ast.Constant) and isinstance(
                        node.value.value, str
                    ):
                        props.help = node.value.value  # type:ignore
                    elif isinstance(node.value, (_ast.List, _ast.Tuple)):
                        props.flags = _ast.literal_eval(node.value)
                else:
                    argument = None

        bases = base.__bases__  # type:ignore

    return argsprops


class _Parser(_argparse.ArgumentParser, _ty.Generic[_T]):
    def parse_args(self, args=None, namespace: _T | None = None) -> _T:  # type:ignore
        raise NotImplementedError()

    def parse_known_args(  # type:ignore
        self, args=None, namespace: _T | None = None
    ) -> tuple[_T, list[str]]:
        raise NotImplementedError()


class Args(_argparse.Namespace):
    @classmethod
    def _getargs_(cls):
        typehints = _ty.get_type_hints(cls, include_extras=True)
        argsprops = _get_clsargs_props(cls)
        args: list[ArgumentBuilder] = []
        for name, type in typehints.items():
            if hasattr(type, "__metadata__"):
                if type.__metadata__[0] is _argparse.SUPPRESS:
                    continue
                options = {}
                for opts in type.__metadata__:
                    options.update(
                        opts if isinstance(opts, _ty.Mapping) else opts.__dict__
                    )
                type = type.__origin__
                builder = Argument.from_type(type, **options)._argbuilder_
            elif is_argument(type):
                builder = type._argbuilder_
            else:
                builder = Argument.from_type(type)._argbuilder_
            props = argsprops.get(name, ArgAnnotations())
            args.append(
                builder(
                    name,
                    props,
                    getattr(cls, name, _Missing),
                )
            )
        return args

    @classmethod
    def build_parser(
        cls,
        subparser: _argparse._SubParsersAction | None = None,
        name: str | None = None,  # type:ignore
        parents: _ty.Sequence[_argparse.ArgumentParser] = [],
        **kwargs,
    ):
        if subparser:
            method = subparser.add_parser
        else:
            method = _argparse.ArgumentParser

        name: str = name or getattr(cls, "_parsername_", None) or cls.__name__
        kwargs.setdefault("description", cls.__doc__ or "")
        parser = _ty.cast(
            _Parser[_ty.Self],
            method(name, parents=parents, **kwargs),
        )

        def parse_known_args(args, namespace=None):
            parsed, unk = _argparse.ArgumentParser.parse_known_args(
                parser, args, namespace  # type:ignore
            )
            return cls(**parsed.__dict__), unk

        parser.parse_known_args = parse_known_args  # type:ignore

        for arg in cls._getargs_():
            _action = None
            for action in parser._actions:
                if action.dest == arg.name:
                    _action = action
            if not _action:
                _action = arg.add_to_parser(parser)
            setattr(cls, f"_action_{_action.dest}", _action)

        return parser


class UpdateAction(_argparse.Action):
    def __call__(  # type:ignore
        self, parser, namespace, values: dict, option_string=None
    ):
        items: dict = getattr(namespace, self.dest, {})
        items = _copy.deepcopy(items)
        items.update(values or {})
        setattr(namespace, self.dest, items)


def parse_loglevels(text: str, itemdivider: str = ",", valkey_separator=":"):
    levels: dict[str, int] = {}
    levelmapping = _logging.getLevelNamesMapping()

    for entry in text.split(itemdivider):
        name, *level = entry.split(valkey_separator, maxsplit=1)
        if not level:
            level = name
            name = ""
        else:
            level = level[0]
        level = levelmapping.get(level)
        if level is not None:
            levels[name] = level
    return levels


class LoggingArgs(Args):
    loglevels: _ty.Annotated[
        dict[str, int], NS(type=parse_loglevels, action=UpdateAction)
    ] = {}
    "Log Levels"
    ("--loglevel",)  # type:ignore

    verbose: _ty.Annotated[
        int, NS(action="count", help=lambda: _logging.VERBOSE_HELP)
    ] = 0
    "Verbose level"
    ("-v",)  # type:ignore

    def verbose_as_loglevel(self):
        loglevel = (
            list(_logging.VERBOSE_LEVELS.keys()).index(_logging.INFO)
            if self.verbose == _logging.NOTSET
            else self.verbose
        )
        loglevel = min(
            loglevel,
            len(_logging.VERBOSE_LEVELS) - 1,
        )
        return list(_logging.VERBOSE_LEVELS.keys())[loglevel]

    def set_loglevels(self):
        loglevels = self.loglevels.copy()
        loglevels.setdefault("", LoggingArgs.verbose_as_loglevel(self))
        for name, level in loglevels.items():
            _logging.getLogger(name).setLevel(level)

        return loglevels


_SUBPARSERACTION_CALL = _argparse._SubParsersAction.__call__


def add_help_argument(parser: _argparse.ArgumentParser):
    return parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=_argparse.SUPPRESS,
        help=("show this help message and exit"),
    )


def disable_subparser_check(action: _argparse._SubParsersAction):
    action.choices = None  # type:ignore
    action_called = False

    def action_call(
        self: _argparse._SubParsersAction,
        parser: _argparse.ArgumentParser,
        namespace: _argparse.Namespace,
        values,
        option_string=None,
    ):
        nonlocal action_called
        parser_name = values[0]
        arg_strings = values[1:]

        if not action_called:
            setattr(namespace, self.dest, parser_name)
            action_called = True

        subnamespace, arg_strings = parser.parse_known_args(arg_strings, namespace)
        for key, value in vars(subnamespace).items():
            setattr(namespace, key, value)

        if arg_strings:
            vars(namespace).setdefault(_argparse._UNRECOGNIZED_ARGS_ATTR, [])
            getattr(namespace, _argparse._UNRECOGNIZED_ARGS_ATTR).extend(arg_strings)

    _argparse._SubParsersAction.__call__ = action_call


def enable_subparser_check(action: _argparse._SubParsersAction):
    _argparse._SubParsersAction.__call__ = _SUBPARSERACTION_CALL
    action.choices = action._name_parser_map


_HELPACTION_CALL = _argparse._HelpAction.__call__


def prerun_parse(
    parser: _argparse.ArgumentParser, argv: _ty.Sequence[str] | None = None
):
    subparser = None
    if parser._subparsers:
        for action in parser._subparsers._actions:
            if isinstance(action, _argparse._SubParsersAction):
                subparser = action
    _argparse._HelpAction.__call__ = lambda *args: ...  # type: ignore
    if subparser:
        required = subparser.required
        subparser.required = False
        disable_subparser_check(subparser)
    args, _ = parser.parse_known_args(argv)
    if subparser:
        enable_subparser_check(subparser)
        subparser.required = required  # type: ignore
    _argparse._HelpAction.__call__ = _HELPACTION_CALL
    return args
