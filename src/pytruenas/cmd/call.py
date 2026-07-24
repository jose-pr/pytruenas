"""Call an arbitrary TrueNAS middleware method and print its JSON result.

Unlike ``query`` (which only covers queryable ``<namespace>.query`` methods),
``call`` invokes any method by its dotted name, e.g. ``system.info``,
``core.ping``, ``pool.dataset.details``. Parameters are passed with ``-p`` as
JSON values (repeatable), so the trailing positionals stay the target host(s).

Put ``-p`` values *before* the method or *after* the targets — argparse cannot
split a ``-p VALUE`` placed between the method and the trailing target
positionals::

    pytruenas call -p '{"username": "svc"}' user.create nas1
    pytruenas call user.create nas1 -p '{"username": "svc"}'

duho 0.5.0's flag-between-positionals reorder fix does not cover this: it
patches ``Args._initparser_``'s ``parse_known_args``, which only the root
parser and duho's own declarative ``_subcommands_`` tree go through. A module
command's subparser (this one) is built by ``duho.discovery``/
``duho.runtime._register_module_command`` via plain
``subparsers.add_parser(...)`` and dispatched by stdlib argparse's own
``_SubParsersAction``, never reaching the patched method -- see the duho
finding ``2026-07-24_module_command_subparsers_bypass_positional_reorder.md``.
"""

from __future__ import annotations

import json
from logging import Logger

from duho import Arg, NS

from pytruenas import TrueNASClient
from pytruenas.utils.cmd import PyTrueNASArgs


class Args(PyTrueNASArgs):
    """Declared CLI fields for ``call`` (added ahead of the trailing targets)."""

    method: str
    "Method to call, e.g. system.info or core.ping"
    ("method",)  # type: ignore

    # duho 0.5.0+ already defaults a list-typed OPTION to action="append",
    # nargs=None (one value per occurrence, `-p a -p b`) -- no explicit
    # NS(action=..., nargs=...) needed here.
    params: "Arg[list[str], NS(metavar='JSON')]" = []
    """A parameter as a JSON value (repeatable); a value that is not valid JSON
    is passed as a plain string."""
    ("--param", "-p")  # type: ignore


def _parse_param(raw: str):
    """A param is a JSON value; fall back to the raw string if it isn't JSON."""
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        return raw


def run(client: TrueNASClient, args: Args, logger: Logger):
    params = [_parse_param(p) for p in (args.params or [])]
    logger.info("Calling %s with %d param(s)", args.method, len(params))
    result = client.api[args.method](*params)
    # default=str so ejson-decoded datetimes/sets serialize instead of raising.
    print(json.dumps(result, default=str))
