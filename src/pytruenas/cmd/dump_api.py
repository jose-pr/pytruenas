"""Dump the full API definition of a TrueNAS host as JSON."""

from pytruenas import TrueNASClient
from pytruenas.utils.cmd import PyTrueNASArgs as PyTrueNASCmd, emit_json
from logging import Logger

import json


def run(client: TrueNASClient, args: PyTrueNASCmd, logger: Logger):

    logger.info("Generating api at server")
    # One atomic write through the shared helper: `print()` is two writes, so
    # under --parallel two dumps interleaved mid-line and neither parsed.
    emit_json(client.dump_api(), args)
