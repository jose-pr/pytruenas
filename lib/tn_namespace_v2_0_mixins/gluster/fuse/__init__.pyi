
from pytruenas import TrueNASClient
from pytruenas.base import Namespace

import typing
class GlusterFuse(
    Namespace
    ):
    _namespace:typing.Literal['gluster.fuse']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def is_mounted(self, 
        glusterfuse_mounted:'GlusterfuseMounted'={},
    /) -> 'bool': 
        """
        Check if gluster volume is FUSE mounted locally.
        
        `name` String representing name of the gluster volume

        Parameters
        ----------
        glusterfuse_mounted:
            glusterfuse_mounted
        Returns
        -------
        bool:
            is_mounted
        """
        ...
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
    @typing.overload
    def mount(self, 
        gluserfuse_mount:'GluserfuseMount'={},
    /) -> 'bool': 
        """
        Mount a gluster volume using the gluster FUSE client.
        
        `name` String representing the name of the gluster volume
        `all` Boolean if True locally FUSE mount all detected
                gluster volumes
        `raise` Boolean if True raise a CallError if the FUSE mount
                fails
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        gluserfuse_mount:
            gluserfuse_mount
        Returns
        -------
        bool:
            mount
        """
        ...
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
    @typing.overload
    def umount(self, 
        glusterfuse_umount:'GlusterfuseUmount'={},
    /) -> 'bool': 
        """
        Unmount a locally FUSE mounted gluster volume.
        
        `name` String representing the name of the gluster volume
        `all` Boolean if True umount all locally detected FUSE
                mounted gluster volumes
        `raise` Boolean if True raise a CallError if the FUSE mount
                fails
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        glusterfuse_umount:
            glusterfuse_umount
        Returns
        -------
        bool:
            umount
        """
        ...
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

