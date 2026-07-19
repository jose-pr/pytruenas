"""Generate typed API stubs (.pyi) for a TrueNAS API version.

Dumps the middleware API definition (or reads a cached dump) and writes a
package of ``.pyi`` stubs describing every namespace and method, so editors and
type checkers understand ``client.api.<namespace>.<method>(...)`` calls.
"""

from __future__ import annotations

import argparse
import json
from logging import Logger
from pathlib import Path

from pytruenas import TrueNASClient, codegen
from pytruenas.utils.cmd import PyTrueNASArgs, register_targets


class Args(PyTrueNASArgs):
    api_version: str
    path: Path
    api_cache: Path


def register(parser: argparse.ArgumentParser, args: PyTrueNASArgs, logger: Logger):
    parser.add_argument(
        "--api-version",
        type=str,
        default=None,
        help="API version to generate (default: the newest in the dump)",
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path("typings"),
        help="Output directory for the generated stubs (default: ./typings)",
    )
    parser.add_argument(
        "--api-cache",
        type=Path,
        default=None,
        help="Path to cache the API dump JSON (read if present, written if not)",
    )
    # Targets are the trailing positionals.
    register_targets(parser)


def run(client: TrueNASClient, args: Args, logger: Logger):
    cache = args.api_cache
    if cache is not None and cache.exists():
        logger.info("Reading cached API dump from %s", cache)
        apidump = json.loads(cache.read_text(encoding="utf-8"))
    else:
        logger.info("Dumping API definition from server")
        apidump = client.dump_api()
        if cache is not None:
            cache.write_text(json.dumps(apidump), encoding="utf-8")
            logger.info("Cached API dump at %s", cache)

    versions = apidump["versions"]
    available = [v["version"] for v in versions]
    if args.api_version:
        version = next((v for v in versions if v["version"] == args.api_version), None)
        if version is None:
            raise SystemExit(
                f"version {args.api_version!r} not found; available: {', '.join(available)}"
            )
    else:
        # The dump lists versions newest-first; default to the newest.
        version = versions[0]

    logger.info("Generating typings for %s into %s", version["version"], args.path)
    codegen.Codegen().generate(version, args.path)
    logger.info("Done")
