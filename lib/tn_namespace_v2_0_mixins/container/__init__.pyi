
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin
from enum import Enum
import typing
class Container(
    ConfigMixin,
    Namespace
    ):
    _namespace:typing.Literal['container']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def config(self, 
    /) -> 'ContainerEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        ContainerEntry:
            container_entry
        """
        ...
    @typing.overload
    def prune(self, 
        prune_options:'PruneOptions',
    /) -> 'PrunedResources': 
        """
        Prune unused images/containers. This will by default remove any dangling images.
        
        `prune_options.remove_unused_images` when set will remove any container image which is not being used by any
        container.

        Parameters
        ----------
        prune_options:
            prune_options
        Returns
        -------
        PrunedResources:
            Example(s):
            ```
            {
                "images": {
                    "ImagesDeleted": [
                        {
                            "id": "sha256:883e787c00d4208d75fc3e85d100ce64b517e49a2468f0e7f084cf05d16f3e46",
                            "Untagged": "quay.io/skopeo/stable:latest"
                        },
                        {
                            "id": "sha256:883e787c00d4208d75fc3e85d100ce64b517e49a2468f0e7f084cf05d16f3e46",
                            "Untagged": "quay.io/skopeo/stable:latest2"
                        }
                    ],
                    "SpaceReclaimed": 260858493
                }
            }
            ```
        """
        ...
    @typing.overload
    def update(self, 
        container_update:'ContainerUpdate',
    /) -> 'ContainerUpdateReturns': 
        """
        When `enable_image_updates` is set, system will check if existing container images need to be updated. System
        will basically check if we have an updated image hash available for the same tag available and if we do,
        user is alerted to update the image.
        A use case for unsetting this variable can be rate limits for docker registries, as each time we check if a
        single image needs update, we consume the rate limit and eventually it can hinder operations if the number
        of images to be checked is a lot.

        Parameters
        ----------
        container_update:
            container_update
        Returns
        -------
        ContainerUpdateReturns:
            container_update_returns
        """
        ...
    ContainerEntry = typing.TypedDict('ContainerEntry', {
            'enable_image_updates':'bool',
            'id':'int',
    })
    ContainerUpdate = typing.TypedDict('ContainerUpdate', {
            'enable_image_updates':'bool',
    })
    ContainerUpdateReturns = typing.TypedDict('ContainerUpdateReturns', {
            'enable_image_updates':'bool',
            'id':'int',
    })
    PruneOptions = typing.TypedDict('PruneOptions', {
            'remove_unused_images':'bool',
    })
    PrunedResources = typing.TypedDict('PrunedResources', {
            'images':'dict[str]',
    })
