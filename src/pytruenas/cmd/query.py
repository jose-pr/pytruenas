"""Query a TrueNAS namespace and print the matching records as JSON."""

from __future__ import annotations

import json
from logging import Logger

from duho import Arg, NS

from pytruenas import TrueNASClient
from pytruenas.utils.cmd import PyTrueNASArgs


class Args(PyTrueNASArgs):
    """Declared CLI fields for ``query`` (added ahead of the trailing targets)."""

    namespace: str
    "API namespace, e.g. user or pool.dataset"
    ("namespace",)  # type: ignore

    # NOTE: not -q -- duho's LoggingArgs owns -q (quiet), and duho.app builds each
    # subcommand parser with parents=[root], so global short flags are inherited
    # and would collide.
    # duho 0.5.0+ already defaults a list-typed OPTION to action="append",
    # nargs=None (one value per occurrence, `-f a -f b`) -- no explicit
    # NS(action=..., nargs=...) needed here.
    query: "Arg[list[str], NS(metavar='KEY=VALUE')]" = []
    "Filter on a field (repeatable), e.g. -f username=root"
    ("--filter", "-f")  # type: ignore


def run(client: TrueNASClient, args: Args, logger: Logger):
    filter = {}
    for entry in args.query or []:
        if not entry:
            continue
        key, _, value = entry.partition("=")
        filter[key] = value

    logger.info("Querying %s with %s", args.namespace, filter or "no filter")
    result = client.api[args.namespace]._query(**filter)
    # default=str so ejson-decoded datetimes/sets serialize instead of raising.
    print(json.dumps(result, default=str))
