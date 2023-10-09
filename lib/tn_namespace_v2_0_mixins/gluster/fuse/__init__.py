
from pytruenas.base import Namespace

import typing
from enum import Enum

class GlusterFuse(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'gluster.fuse')

    GlusterfuseMounted = typing.TypedDict('GlusterfuseMounted', {
            'name':'str',
    })
    GluserfuseMount = typing.TypedDict('GluserfuseMount', {
            'name':'str',
            'all':'bool',
            'raise':'bool',
    })
    GlusterfuseUmount = typing.TypedDict('GlusterfuseUmount', {
            'name':'str',
            'all':'bool',
            'raise':'bool',
    })
