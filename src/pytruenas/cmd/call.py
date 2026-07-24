"""Call an arbitrary TrueNAS middleware method and print its JSON result.

Unlike ``query`` (which only covers queryable ``<namespace>.query`` methods),
``call`` invokes any method by its dotted name, e.g. ``system.info``,
``core.ping``, ``pool.dataset.details``. Parameters are passed with ``-p`` as
JSON values (repeatable), so the trailing positionals stay the target host(s).

Any ordering of ``-p`` relative to ``method``/the trailing targets now parses,
including between them (``pytruenas call method -p '{"a": 1}' nas1``) -- as of
duho >=0.5.1, whose flag-between-positionals reorder fix extends to a module
command's subparser (this one); 0.5.0 alone only covered duho's own
declarative ``_subcommands_`` tree. Earlier duho versions required ``-p``
before ``method`` or after the targets; see the duho finding
``2026-07-24_module_command_subparsers_bypass_positional_reorder.md`` for the
history if this regresses.
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

    # duho >=0.5.0 defaults a list-typed OPTION to action="append", nargs=None
    # (one value per occurrence, `-p a -p b`) -- no explicit override needed.
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
