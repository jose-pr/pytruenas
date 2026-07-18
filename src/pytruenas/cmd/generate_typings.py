"""
Get the supported api definitions from a TrueNAS host
"""

from pytruenas import TrueNASClient
from pytruenas.utils.cmd import PyTrueNASArgs as PyTrueNASCmd
from logging import Logger
import argparse

import json

from pytruenas import codegen
from pathlib import Path


class Args(PyTrueNASCmd):
    api_version: str
    path: Path
    api_cache: Path


def register(parser: argparse.ArgumentParser, args: PyTrueNASCmd, logger: Logger):
    parser.add_argument("--api-version", type=str)
    parser.add_argument("--path", type=Path)
    parser.add_argument("--api-cache", type=Path)


def run(client: TrueNASClient, args: Args, logger: Logger):
    if not args.api_cache.exists():
        logger.info("Generating api at server")
        args.api_cache.write_text(json.dumps(client.dump_api()))
    
    apidump:list[codegen._api.Version]=json.loads(args.api_cache.read_text())
    version = None
    for _version in apidump['versions']:
        if _version["version"] == args.api_version:
            version = _version
            break
    if not version:
        raise Exception('Version not found in api dump')

    gen = codegen.Codegen()
    gen.generate(version, args.path)