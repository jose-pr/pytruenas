"""Dump the full API definition of a TrueNAS host as JSON."""

from logging import Logger

from pytruenas import TrueNASClient
from pytruenas.cli import PyTrueNASArgs, emit_json


def run(client: TrueNASClient, args: PyTrueNASArgs, logger: Logger):
    logger.info("Generating api at server")
    # One locked write: concurrent targets' dumps cannot interleave mid-line.
    emit_json(client.dump_api(), args)
