"""
Get the supported api definitions from a TrueNAS host
"""

import argparse
import json
from logging import Logger

from pytruenas import TrueNASClient
from pytruenas.cli import PyTrueNASArgs


class Args(PyTrueNASArgs):
    query: list[str]
    namespace: str


def register(parser: argparse.ArgumentParser, args: PyTrueNASArgs, logger: Logger):
    parser.add_argument("-q", "--query", action="append")
    parser.add_argument("namespace")


def run(client: TrueNASClient, args: Args, logger: Logger):
    filter = {}
    for entry in args.query:
        if not entry:
            continue
        k, v = entry.split("=")
        filter[k] = v

    logger.info(f"Looking up object from {args.namespace}")

    result = client.api[args.namespace]._query(**filter)

    print(json.dumps(result))
