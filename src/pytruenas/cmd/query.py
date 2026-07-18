"""Query a TrueNAS namespace and print the matching records as JSON."""

from __future__ import annotations

import argparse
import json
from logging import Logger

from pytruenas import TrueNASClient
from pytruenas.utils.cmd import PyTrueNASArgs


class Args(PyTrueNASArgs):
    query: list[str]
    namespace: str


def register(parser: argparse.ArgumentParser, args: PyTrueNASArgs, logger: Logger):
    parser.add_argument(
        "-q",
        "--query",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Filter on a field (repeatable), e.g. -q username=root",
    )
    parser.add_argument("namespace", help="API namespace, e.g. user or pool.dataset")


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
