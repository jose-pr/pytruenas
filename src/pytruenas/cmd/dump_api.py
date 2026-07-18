"""
Get the supported api definitions from a TrueNAS host
"""
from pytruenas import TrueNASClient
from pytruenas.utils.cmd import PyTrueNASArgs as PyTrueNASCmd
from logging import Logger

import json


def run(client:TrueNASClient, args:PyTrueNASCmd, logger:Logger):

    logger.info("Generating api at server")
    apidump = json.dumps(client.dump_api())


    print(apidump)