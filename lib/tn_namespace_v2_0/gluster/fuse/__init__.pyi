
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class GlusterFuse(Namespace):
    _namespace:_ty.Literal['gluster.fuse']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def is_mounted(self, 
        glusterfuse_mounted:'dict[str]'={},
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
    @_ty.overload
    def mount(self, 
        gluserfuse_mount:'dict[str]'={},
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
    @_ty.overload
    def umount(self, 
        glusterfuse_umount:'dict[str]'={},
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
