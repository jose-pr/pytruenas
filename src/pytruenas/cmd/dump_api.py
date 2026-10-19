"""Dump the full API definition of a TrueNAS host as JSON."""

from pytruenas import TrueNASClient
from pytruenas.utils.cmd import PyTrueNASArgs as PyTrueNASCmd, emit_json
from logging import Logger


def run(client: TrueNASClient, args: PyTrueNASCmd, logger: Logger):

    logger.info("Generating api at server")
    # One locked write: concurrent targets' dumps cannot interleave mid-line.
    emit_json(client.dump_api(), args)
