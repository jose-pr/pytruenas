"""
Test loadable script for pytruenas
"""

from logging import Logger

from pytruenas import TrueNASClient
from pytruenas.cli import PyTrueNASArgs

REQUIRED = ["step2"]


def run(client: TrueNASClient, args: PyTrueNASArgs, logger: Logger):
    logger.info(__name__)
