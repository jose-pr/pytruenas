import copy as _copy
import argparse as _argparse
from . import logging as _logging


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


def add_logging_args(parser: _argparse.ArgumentParser):
    _logging.initverbose()

    return (
        parser.add_argument(
            "--loglevel",
            action=UpdateAction,
            default={},
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


class LoggingArgs(_argparse.Namespace):
    loglevels: dict[str, int]
    verbose: int

    def set_loglevels(self):
        loglevel = min(
            self.verbose or list(_logging.VERBOSE_LEVELS.keys()).index(_logging.INFO),
            len(_logging.VERBOSE_LEVELS) - 1,
        )
        loglevel = list(_logging.VERBOSE_LEVELS.keys())[loglevel]
        self.loglevels.setdefault("", loglevel)
        for name, level in self.loglevels.items():
            _logging.getLogger(name).setLevel(level)

        return self.loglevels


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
        global action_called
        action_called = True
        parser_name = values[0]
        arg_strings = values[1:]

        setattr(namespace, self.dest, parser_name)
        subnamespace, arg_strings = parser.parse_known_args(arg_strings, None)
        for key, value in vars(subnamespace).items():
            setattr(namespace, key, value)

    _argparse._SubParsersAction.__call__ = action_call


def enable_subparser_check(action: _argparse._SubParsersAction):
    _argparse._SubParsersAction.__call__ = _SUBPARSERACTION_CALL
    action.required = True
    action.choices = action._name_parser_map


def prerun_parse(parser: _argparse.ArgumentParser):
    subparser = None
    if parser._subparsers:
        for action in parser._subparsers._actions:
            if isinstance(action, _argparse._SubParsersAction):
                subparser = action
    if subparser:
        disable_subparser_check(subparser)
    args, _ = parser.parse_known_args()
    if subparser:
        enable_subparser_check(subparser)
    return args
