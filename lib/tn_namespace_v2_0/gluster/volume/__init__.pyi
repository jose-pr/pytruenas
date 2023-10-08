
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class GlusterVolume(Namespace):
    _namespace:_ty.Literal['gluster.volume']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        glustervolume_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create a gluster volume.
        
        `name` String representing name to be given to the volume
        `bricks` List representing the brick paths
            `peer_name` String representing IP or DNS name of the peer
            `peer_path` String representing the full path of the brick
        
        `replica` Integer representing number of replica bricks
        `arbiter` Integer representing number of arbiter bricks
        `disperse` Integer representing number of disperse bricks
        `disperse_data` Integer representing number of disperse data bricks
        `redundancy` Integer representing number of redundancy bricks
        `force` Boolean, if True ignore potential warnings
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        glustervolume_create:
            glustervolume_create
        Returns
        -------
        dict[str]:
            gluster_volume_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'str',
    /) -> None: 
        """
        Delete a gluster volume.
        
        `id` String representing name of gluster volume
                to be deleted
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        id:
            `id` String representing name of gluster volume
                    to be deleted
        Returns
        -------
        """
        ...
    @_ty.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'dict[str]'={},
    /) -> None: 
        """
        Returns instance matching `id`. If `id` is not found, Validation error is raised.
        
        Please see `query` method documentation for `options`.

        Parameters
        ----------
        id:
            Returns instance matching `id`. If `id` is not found, Validation error is raised.
        query_options_get_instance:
            query-options-get_instance
        Returns
        -------
        """
        ...
    @_ty.overload
    def info(self, 
        volume_info:'dict[str]'={},
    /) -> 'list': 
        """
        Return information about gluster volume(s).
        
        `name` String representing name of gluster volume

        Parameters
        ----------
        volume_info:
            volume_info
        Returns
        -------
        list:
            volumes
        """
        ...
    @_ty.overload
    def list(self, 
    /) -> 'list': 
        """
        Return list of gluster volumes.

        Parameters
        ----------
        Returns
        -------
        list:
            volumes
        """
        ...
    @_ty.overload
    def optreset(self, 
        volume_optreset:'dict[str]'={},
    /) -> None: 
        """
        Reset volumes options.
            If `opt` is not provided, then all options
            will be reset.
        
        `name` String representing name of gluster volume
        `opt` String representing name of the option to reset
        `force` Boolean, if True forcefully reset option(s)

        Parameters
        ----------
        volume_optreset:
            volume_optreset
        Returns
        -------
        """
        ...
    @_ty.overload
    def optset(self, 
        volume_optset:'dict[str]'={},
    /) -> None: 
        """
        Set gluster volume options.
        
        `name` String representing name of gluster volume
        `opts` Dict where
            --key-- is the name of the option
            --value-- is the value to be given to the option
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        volume_optset:
            volume_optset
        Returns
        -------
        """
        ...
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @_ty.overload
    def quota(self, 
        volume_quota:'dict[str]'={},
    /) -> None: 
        """
        Enable/Disable the quota for a given gluster volume.
        
        `name` String representing name of gluster volume
        `enable` Boolean, if True enable quota else disable it
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        volume_quota:
            volume_quota
        Returns
        -------
        """
        ...
    @_ty.overload
    def restart(self, 
        volume_restart:'dict[str]'={},
    /) -> None: 
        """
        Restart a gluster volume.
        
        `name` String representing name of gluster volume
        `force` Boolean, if True forcefully restart the gluster volume

        Parameters
        ----------
        volume_restart:
            volume_restart
        Returns
        -------
        """
        ...
    @_ty.overload
    def start(self, 
        volume_start:'dict[str]'={},
    /) -> None: 
        """
        Start a gluster volume.
        
        `name` String representing name of gluster volume
        `force` Boolean, if True forcefully start the gluster volume
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        volume_start:
            volume_start
        Returns
        -------
        """
        ...
    @_ty.overload
    def status(self, 
        volume_status:'dict[str]'={},
    /) -> 'list': 
        """
        Return detailed information about gluster volume.
        
        `name` String representing name of gluster volume
        `verbose` Boolean, If False, only return brick information

        Parameters
        ----------
        volume_status:
            volume_status
        Returns
        -------
        list:
            volumes
        """
        ...
    @_ty.overload
    def stop(self, 
        volume_stop:'dict[str]'={},
    /) -> None: 
        """
        Stop a gluster volume.
        
        `name` String representing name of gluster volume
        `force` Boolean, if True forcefully stop the gluster volume
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        volume_stop:
            volume_stop
        Returns
        -------
        """
        ...
