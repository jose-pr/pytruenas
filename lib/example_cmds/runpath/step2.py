"""
Test loadable script for pytruenas
"""

from logging import Logger

from pytruenas import TrueNASClient
from pytruenas.cli import PyTrueNASArgs


def run(client: TrueNASClient, args: PyTrueNASArgs, logger: Logger):

    logger.info(__name__)
