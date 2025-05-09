import argparse as _argparse
import copy as _copy
import typing as _ty

from ..utils import logging as _logging
from .arg import *


def pop_action(parser: _argparse.ArgumentParser, name: str):
    index = None
    for idx, action in enumerate(parser._actions):
        if action.dest == name:
            index = idx
            break
    if index is not None:
        action = parser._actions.pop(index)
        for k in action.option_strings:
            parser._option_string_actions.pop(k)
        return action
    raise KeyError(name)


def insert_action(
    parser: _argparse.ArgumentParser, action: _argparse.Action, index: int = -1
):
    parser._actions.insert(index, action)
    for k in action.option_strings:
        parser._option_string_actions[k] = action


def Extend(split: str | _ty.Callable[[str], _ty.Iterable], **kwargs):
    kwargs.setdefault("default", [])
    if isinstance(split, str):
        ty: _ty.Callable[[str], list] = lambda x: x.split(split)  # type:ignore
    else:

        def ty(text: str):
            result = split(text)
            if isinstance(result, list):
                return result
            return list(result)

    return _argparse.Namespace(type=ty, action="extend", kwargs=kwargs)


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
