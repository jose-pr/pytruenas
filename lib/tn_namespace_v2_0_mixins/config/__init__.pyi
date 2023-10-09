
from pytruenas import TrueNASClient
from pytruenas.base import Namespace

import typing
class Config(
    Namespace
    ):
    _namespace:typing.Literal['config']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def reset(self, 
        options:'Options'={},
    /) -> None: 
        """
        Reset database to configuration defaults.
        
        If `reboot` is true this job will reboot the system after its completed with a delay of 10
        seconds.

        Parameters
        ----------
        options:
            options
        Returns
        -------
        """
        ...
    Options = typing.TypedDict('Options', {
            'reboot':'bool',
    })
    Configsave = typing.TypedDict('Configsave', {
            'secretseed':'bool',
            'pool_keys':'bool',
            'root_authorized_keys':'bool',
            'gluster_config':'bool',
    })
    @typing.overload
    def save(self, 
        configsave:'Configsave'={},
    /) -> None: 
        """
        Create a tar file of security-sensitive information. These options select which information
        is included in the tar file:
        
        `secretseed` bool: When true, include password secret seed.
        `pool_keys` bool: IGNORED and DEPRECATED as it does not apply on SCALE systems.
        `root_authorized_keys` bool: When true, include "/root/.ssh/authorized_keys" file for the root user.
        `gluster_config` bool: When true, include the directory that stores the gluster configuration files.
        
        If none of these options are set, the tar file is not generated and the database file is returned.

        Parameters
        ----------
        configsave:
            configsave
        Returns
        -------
        """
        ...
    Options = typing.TypedDict('Options', {
            'reboot':'bool',
    })
    Configsave = typing.TypedDict('Configsave', {
            'secretseed':'bool',
            'pool_keys':'bool',
            'root_authorized_keys':'bool',
            'gluster_config':'bool',
    })
    @typing.overload
    def upload(self, 
    /) -> None: 
        """
        Accepts a configuration file via job pipe.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    Options = typing.TypedDict('Options', {
            'reboot':'bool',
    })
    Configsave = typing.TypedDict('Configsave', {
            'secretseed':'bool',
            'pool_keys':'bool',
            'root_authorized_keys':'bool',
            'gluster_config':'bool',
    })

