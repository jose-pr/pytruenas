"""Dump the API definition of a TrueNAS host as JSON (current version only by default)."""

from logging import Logger

from pytruenas import TrueNASClient
from pytruenas.cli import PyTrueNASArgs, emit_json


class Args(PyTrueNASArgs):
    """Declared CLI fields for ``dump-api``."""

    all_versions: bool = False
    "Every API version the appliance serves, not only the current one"


def run(client: TrueNASClient, args: Args, logger: Logger):
    logger.info("Generating api at server")
    # One locked write: concurrent targets' dumps cannot interleave mid-line.
    emit_json(client.dump_api(all_versions=args.all_versions), args)
