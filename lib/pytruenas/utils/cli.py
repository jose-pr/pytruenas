import argparse as _argparse
import ast as _ast
import copy as _copy
import inspect as _inspect
import types as _types
import typing as _ty

from . import logging as _logging


class _Missing: ...


_type = type
MissingType = _type[_Missing]


class Argument(_ty.Protocol):
    @classmethod
    def _argbuilder_(
        cls,
        name: str,
        type: _type,  # type: ignore
        docstring: str,
        default: None | object | MissingType,
    ):
        help = docstring
        flags = ("--" + name.replace("_", "-"),)
        if help.startswith("\\"):
            flags, help = help[1:].split("\\", maxsplit=1)
            flags = flags.split(",")
        required = None
        origin = _ty.get_origin(type)
        args = _ty.get_args(type)
        if origin:
            if origin is _ty.Union and _types.NoneType in args:
                args = [a for a in args if a is not _types.NoneType]
                required = False
                if len(args) == 1:
                    type = args[0]
            if origin is _ty.Union or origin is _types.UnionType and len(args) > 1:

                def type(text: str):
                    for ty in args:
                        try:
                            return ty(text)
                        except:
                            pass
                    raise ValueError(text, args)

        return ArgumentBuilder(
            name=name,
            flags=flags,
            type=type,
            default=default,
            help=help,
            required=required,
        )


def is_argument(ty: type) -> _ty.TypeGuard[Argument]:
    builder_factory = getattr(ty, "_argbuilder_", None)
    return callable(builder_factory)


class ArgumentBuilder(_argparse.Namespace):
    name: str
    flags: list[str]
    type: _type | str
    default: None | object | MissingType
    help: str
    required: bool | None = None
    action: str | _type[_argparse.Action] | None = None

    def _kwargs(self):
        kwargs = {}
        if self.required is not None:
            kwargs["required"] = self.required

        if self.default is not _Missing:
            kwargs["default"] = self.default

        if self.action:
            kwargs["action"] = self.action

        return kwargs

    def add_to_parser(self, parser: _argparse.ArgumentParser):

        return parser.add_argument(
            *self.flags,
            dest=self.name,
            help=self.help,
            type=self.type,
            **self._kwargs(),
        )


def _get_clsargs_docstrings(cls):
    docstrings: dict[str, str] = {}
    bases = [cls]
    while bases:
        for base in bases:
            try:
                source = _inspect.getsource(base)
            except TypeError:
                continue
            tree = _ty.cast(_ast.ClassDef, _ast.parse(source).body[0])
            argument = None
            for node in tree.body:
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
                elif (
                    isinstance(node, _ast.Expr)
                    and argument
                    and isinstance(node.value, _ast.Constant)
                    and isinstance(node.value.value, str)
                ):
                    if argument not in docstrings:
                        docstrings[argument] = node.value.value
                argument = None

        bases = base.__bases__  # type:ignore

    return docstrings


class Args(_argparse.Namespace):
    @classmethod
    def _getargs_(cls):
        typehints = _ty.get_type_hints(cls)
        docstrings = _get_clsargs_docstrings(cls)
        args: list[ArgumentBuilder] = []
        for name, type in typehints.items():
            if is_argument(type):
                builder = type._argbuilder_
            else:
                builder = Argument._argbuilder_

            args.append(
                builder(
                    name,
                    _ty.cast(_type, type),
                    docstrings.get(name, ""),
                    getattr(cls, name, _Missing),
                )
            )
        return args

    @classmethod
    def build_parser(
        cls, subparser: _argparse._SubParsersAction | None = None, **kwargs
    ):
        if subparser:
            method = subparser.add_parser
        else:
            method = _argparse.ArgumentParser

        parser = method(cls.__name__, usage=cls.__doc__ or "", **kwargs)

        for arg in cls._getargs_():
            arg.add_to_parser(parser)

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


def add_logging_args(
    parser: _argparse.ArgumentParser, default_levels: dict[str, int] = {}
):
    _logging.initverbose()

    return (
        parser.add_argument(
            "--loglevel",
            action=UpdateAction,
            default={**default_levels},
            type=parse_loglevels,
            dest="loglevels",
        ),
        parser.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=0,
            help=_logging.VERBOSE_HELP,
        ),
    )


class LogLevels(dict[str, int], Argument):

    @classmethod
    def _argbuilder_(
        cls,
        name: str,
        type: type,
        docstring: str,
        default: _types.NoneType | object | type[_Missing],
    ):
        type = parse_loglevels  # type:ignore
        arg = super()._argbuilder_(name, type, docstring, {})
        arg.action = UpdateAction
        return arg


class LoggingArgs(Args):
    loglevels: LogLevels
    """\\--loglevel\\Log Levels"""

    verbose: int = 0

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

        return _ty.cast(LogLevels, loglevels)


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
