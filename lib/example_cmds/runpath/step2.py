"""
Test loadable script for pytruenas
"""
from pytruenas import TrueNASClient
from pytruenas.utils.cmd import PyTrueNASArgs
from logging import Logger


def run(client:TrueNASClient, args:PyTrueNASArgs, logger:Logger):

    logger.info(__name__)
