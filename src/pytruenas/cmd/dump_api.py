"""Dump the full API definition of a TrueNAS host as JSON."""
from pytruenas import TrueNASClient
from pytruenas.utils.cmd import PyTrueNASArgs as PyTrueNASCmd, register_targets
from logging import Logger

import json


def register(parser, args, logger):
    # No command-specific positionals: targets are the only positionals.
    register_targets(parser)


def run(client:TrueNASClient, args:PyTrueNASCmd, logger:Logger):

    logger.info("Generating api at server")
    apidump = json.dumps(client.dump_api())


    print(apidump)