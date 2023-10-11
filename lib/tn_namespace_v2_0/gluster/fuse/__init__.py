
from pytruenas.base import Namespace

import typing
from enum import Enum

class GlusterFuse(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'gluster.fuse')

    GluserfuseMount = typing.TypedDict('GluserfuseMount', {
            'name':'str',
            'all':'bool',
            'raise':'bool',
    })
    GlusterfuseMounted = typing.TypedDict('GlusterfuseMounted', {
            'name':'str',
    })
    GlusterfuseUmount = typing.TypedDict('GlusterfuseUmount', {
            'name':'str',
            'all':'bool',
            'raise':'bool',
    })
