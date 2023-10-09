
from pytruenas.base import Namespace

import typing
class Container(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'container')

    ContainerEntry = typing.TypedDict('ContainerEntry', {
            'enable_image_updates':'bool',
            'id':'int',
    })
    PruneOptions = typing.TypedDict('PruneOptions', {
            'remove_unused_images':'bool',
    })
    PrunedResources = typing.TypedDict('PrunedResources', {
            'images':'dict[str]',
    })
    ContainerUpdate = typing.TypedDict('ContainerUpdate', {
            'enable_image_updates':'bool',
    })
    ContainerUpdateReturns = typing.TypedDict('ContainerUpdateReturns', {
            'enable_image_updates':'bool',
            'id':'int',
    })
