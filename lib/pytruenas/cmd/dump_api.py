"""
Get the supported api definitions from a TrueNAS host
"""

import json
from logging import Logger

from pytruenas.utils.cmd import PyTrueNASArgs

from pytruenas import TrueNASClient


def run(client: TrueNASClient, args: PyTrueNASArgs, logger: Logger):

    logger.info("Generating api at server")
    apidump = json.dumps(client.dump_api())

    print(apidump)
