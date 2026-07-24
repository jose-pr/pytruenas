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

    # nargs=None pins ONE value per -p (`-p a -p b`); duho would otherwise infer
    # nargs='*' from list[str], and a greedy `-p` swallows the trailing targets.
    params: "Arg[list[str], NS(action='append', metavar='JSON', nargs=None)]" = []
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
