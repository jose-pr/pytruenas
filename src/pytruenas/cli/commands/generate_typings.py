"""Generate typed API stubs (.pyi) for a TrueNAS API version.

Reads the middleware API definition from the target (``client.dump_api()``,
cached per host and version) or from a dump file, and writes a package of
``.pyi`` stubs describing every namespace and method, so editors and
type checkers understand ``client.api.<namespace>.<method>(...)`` calls.
"""

from __future__ import annotations

import gzip
import json
import typing as _ty
from logging import Logger
from pathlib import Path

from duho import Arg, Meta

from pytruenas import TrueNASClient, codegen
from pytruenas.cli import PyTrueNASArgs


class Args(PyTrueNASArgs):
    """Declared CLI fields for ``generate-typings``."""

    api_version: str = None
    "API version to generate (default: the one the appliance runs)"

    path: Path = Path("truenasapi_typings/current")
    "Output directory for the generated stubs (default: ./truenasapi_typings/current)"

    dump: "Arg[_ty.Optional[Path], Meta(metavar='FILE')]" = None
    "Read the API definition from this dump file (JSON, or gzipped) instead of the target"
    ("--from",)  # type: ignore


_GZIP_MAGIC = bytes((0x1F, 0x8B))


def _read_dump(path: Path) -> dict:
    """A ``dump-api`` output or a ``$PYTRUENAS_CACHE`` file: JSON, maybe gzipped."""
    raw = path.read_bytes()
    if raw[:2] == _GZIP_MAGIC:
        raw = gzip.decompress(raw)
    return json.loads(raw.decode("utf-8"))


def run(client: TrueNASClient, args: Args, logger: Logger):
    if args.dump is not None:
        logger.info("Reading the API definition from %s", args.dump)
        apidump = _read_dump(Path(args.dump))
    else:
        logger.info("Dumping API definition from server")
        # Only an older version needs the whole dump; the current one is the
        # pruned dump's only entry.
        apidump = client.dump_api(all_versions=bool(args.api_version))

    versions = apidump["versions"]
    available = [v["version"] for v in versions]
    if args.api_version:
        version = next((v for v in versions if v["version"] == args.api_version), None)
        if version is None:
            # `return 2`, not SystemExit: this runs inside a fan-out worker, and
            # raising there aborted the whole run instead of failing one target.
            logger.error(
                "version %r not found; available: %s",
                args.api_version,
                ", ".join(available),
            )
            return 2
    else:
        # The first entry is the version the appliance runs.
        version = versions[0]

    logger.info("Generating typings for %s into %s", version["version"], args.path)
    codegen.Codegen().generate(version, args.path)
    logger.info("Done")
