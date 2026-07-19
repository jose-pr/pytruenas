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

import argparse
import json
from logging import Logger

from pytruenas import TrueNASClient
from pytruenas.utils.cmd import PyTrueNASArgs, register_targets


class Args(PyTrueNASArgs):
    method: str
    params: list[str]


def register(parser: argparse.ArgumentParser, args: PyTrueNASArgs, logger: Logger):
    parser.add_argument("method", help="Method to call, e.g. system.info or core.ping")
    parser.add_argument(
        "-p",
        "--param",
        dest="params",
        action="append",
        default=[],
        metavar="JSON",
        help="A parameter as a JSON value (repeatable); a value that is not "
        "valid JSON is passed as a plain string.",
    )
    # Targets are the trailing positionals -- added AFTER `method`.
    register_targets(parser)


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
