import argparse as _argparse
import ast as _ast
import copy as _copy
import inspect as _inspect
import types as _types
import typing as _ty

from . import logging as _logging


class _Missing: ...


_type = type


class _Field(_argparse.Namespace):
    name: str
    type: _type | str | _type[_Missing] = _Missing
    default: None | object | _type[_Missing] = _Missing
    docstring: str = _Missing  # type:ignore
    required: bool | None = None

    def add_to_parser(self, parser: _argparse.ArgumentParser):
        name = ["--" + self.name.replace("_", "-")]
        opts = []
        parser_kwargs = {}

        if self.docstring.startswith("\\"):
            *opts, help = self.docstring[1:].split("\\")
            parser_kwargs["help"] = help

        if self.default is not _Missing:
            parser_kwargs["default"] = self.default

        for opt in opts:
            if ":" not in opt:
                name = opt.split(",")
                continue
            opt.split(":")
        parser.add_argument(*name, **parser_kwargs)


def _get_fields(cls):
    fields = {name: _Field(type=hint) for name, hint in _ty.get_type_hints(cls).items()}
    bases = [cls]
    while bases:
        for base in bases:
            try:
                source = _inspect.getsource(base)
            except TypeError:
                continue
            tree = _ty.cast(_ast.ClassDef, _ast.parse(source).body[0])
            field = None
            for node in tree.body:
                if isinstance(node, (_ast.Assign, _ast.AnnAssign)):
                    if hasattr(node, "targets"):
                        target = node.targets[0]  # type:ignore
                    else:
                        target = node.target  # type:ignore
                    if not isinstance(target, _ast.Name):
                        field = None
                    else:
                        field = fields.setdefault(target.id, _Field())
                    continue
                elif (
                    isinstance(node, _ast.Expr)
                    and field
                    and isinstance(node.value, _ast.Constant)
                    and isinstance(node.value.value, str)
                ):
                    field.docstring = node.value.value
                field = None

        bases = base.__bases__  # type:ignore

    for name, field in fields.items():
        default = getattr(cls, name, _Missing)
        if default is not _Missing:
            setattr(field, name, default)
        if field.docstring is _Missing:
            field.docstring = ""
        field.name = name
        if field.type is not _Missing:
            origin = _ty.get_origin(field.type)
            args = _ty.get_args(field.type)
            if origin:
                if origin is _ty.Union and _types.NoneType in args:
                    args = [a for a in args if a is not _types.NoneType]
                    field.required = False
            if field.required is not None:
                field.type = (
                    args[0] if len(args) == 1 else _ty.Union(args)  # type:ignore
                )

    return fields


class Args(_argparse.Namespace):
    @classmethod
    def _args_(cls, parser: _argparse.ArgumentParser):
        for name, field in _get_fields(cls).items():
            print(name, field)  # WIP


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


class LoggingArgs(Args):
    loglevels: dict[str, int]
    """Log Levels"""

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
