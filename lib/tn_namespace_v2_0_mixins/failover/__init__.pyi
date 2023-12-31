
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin
from enum import Enum
import typing
class Failover(
    ConfigMixin,
    Namespace
    ):
    _namespace:typing.Literal['failover']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def become_passive(self, 
    /) -> None: 
        """
        This method is only called manually by the end-user so we fully expect that they
        know what they're doing. Furthermore, this method will only run if failover has NOT
        been administratively disabled. The reason why we only allow this in that scenario
        is because the failover logic (on the other node) will ignore any failover "event"
        that comes in if failover has been administratively disabled. This immediately causes
        the HA system to go into a "faulted" state because the other node will get the VIPs
        but it will not import the zpool and it will not start fenced. Only way out of that
        situation is to manually fix things (import zpool, migrate VIPs, start fenced, etc).
        
        NOTE: The only "safe" way to "become passive" is to use the STCNITH method (similar to STONITH).
        (i.e. Shoot The Current Node In The Head)
        
        This ensures that the current node gets out of the way _completely_ so there is no chance
        of the zpool being imported at the same time on both nodes (which can ultimately end in data corruption).

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def call_remote(self, 
        _method:'str',
        _args:'list',
        _options:'Options',
    /) -> 'typing.Union[str, int, bool, dict[str], list]': 
        """
        Call a method on the other node.
        
        `method` name of the method to be called
        `args` list of arguments to be passed to `method`
        `options` dictionary with following keys
            `timeout`: time to wait for `method` to return
                NOTE: This parameter _ONLY_ applies if the remote
                    client is connected to the other node.
            `job`: whether or not the `method` being called is a job
            `job_return`: if true, will return immediately and not wait
                for the job to complete, otherwise will wait for the
                job to complete
            `callback`: a function that will be called as a callback
                on completion/failure of `method`.
                NOTE: Only applies if `method` is a job
            `connect_timeout`: Maximum amount of time in seconds to wait
                for remote connection to become available.
            `raise_connect_error`: If false, will not raise an exception if a connection error to the other node
                happens, or connection/call timeout happens, or method does not exist on the remote node.

        Parameters
        ----------
        method:
            `method` name of the method to be called
            `args` list of arguments to be passed to `method`
        args:
            `method` name of the method to be called
            `args` list of arguments to be passed to `method`
        options:
            options
        Returns
        -------
        typing.Union[str, int, bool, dict[str], list]:
            call_remote
        """
        ...
    @typing.overload
    def config(self, 
    /) -> 'FailoverEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        FailoverEntry:
            failover_entry
        """
        ...
    @typing.overload
    def control(self, 
        _action:'Action',
        _options:'Options_',
    /) -> None: 
        """
        

        Parameters
        ----------
        action:
            action
        options:
            options
        Returns
        -------
        """
        ...
    @typing.overload
    def force_master(self, 
    /) -> 'bool': 
        """
        Force this controller to become MASTER, if it's not already.

        Parameters
        ----------
        Returns
        -------
        bool:
            force_master
        """
        ...
    @typing.overload
    def get_ips(self, 
    /) -> 'list[str]': 
        """
        Get a list of IPs for which the webUI can be accessed.

        Parameters
        ----------
        Returns
        -------
        list[str]:
            ips
        """
        ...
    @typing.overload
    def hardware(self, 
    /) -> 'str': 
        """
        Returns the hardware type for an HA system.
          ECHOSTREAM (z-series)
          ECHOWARP (m-series)
          LAJOLLA2 (f-series)
          PUMA (x-series)
          BHYVE (HA VMs for CI)
          MANUAL (everything else)

        Parameters
        ----------
        Returns
        -------
        str:
            hardware
        """
        ...
    @typing.overload
    def in_progress(self, 
    /) -> 'bool': 
        """
        Returns True if there is an ongoing failover event.

        Parameters
        ----------
        Returns
        -------
        bool:
            in_progress
        """
        ...
    @typing.overload
    def licensed(self, 
    /) -> 'bool': 
        """
        Checks whether this instance is licensed as a HA unit

        Parameters
        ----------
        Returns
        -------
        bool:
            licensed
        """
        ...
    @typing.overload
    def node(self, 
    /) -> 'str': 
        """
        Returns the slot position in the chassis that
        the controller is located.
          A - First node
          B - Seconde Node
          MANUAL - slot position in chassis could not be determined

        Parameters
        ----------
        Returns
        -------
        str:
            node
        """
        ...
    @typing.overload
    def status(self, 
    /) -> 'str': 
        """
        Get the current HA status.
        
        Returns:
            MASTER
            BACKUP
            ELECTING
            IMPORTING
            ERROR
            SINGLE

        Parameters
        ----------
        Returns
        -------
        str:
            status
        """
        ...
    @typing.overload
    def sync_from_peer(self, 
    /) -> None: 
        """
        Sync database and files from the other controller.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def sync_to_peer(self, 
        _options:'Options__',
    /) -> None: 
        """
        Sync database and files to the other controller.
        
        `reboot` as true will reboot the other controller after syncing.

        Parameters
        ----------
        options:
            options
        Returns
        -------
        """
        ...
    @typing.overload
    def unlock(self, 
        _options:'Options___',
    /) -> 'bool': 
        """
        Unlock datasets in HA, syncing passphrase between controllers and forcing this controller
        to be MASTER importing the pools.

        Parameters
        ----------
        options:
            options
        Returns
        -------
        bool:
            unlock
        """
        ...
    @typing.overload
    def update(self, 
        _failover_update:'FailoverUpdate',
    /) -> 'FailoverUpdateReturns': 
        """
        Update failover state.
        
        `disabled` When true indicates that HA will be disabled.
        `master`  Marks the particular node in the chassis as the master node.
                    The standby node will have the opposite value.
        
        `timeout` is the time to WAIT until a failover occurs when a network
            event occurs on an interface that is marked critical for failover AND
            HA is enabled and working appropriately.
        
            The default time to wait is 2 seconds.
            **NOTE**
                This setting does NOT effect the `disabled` or `master` parameters.

        Parameters
        ----------
        failover_update:
            failover_update
        Returns
        -------
        FailoverUpdateReturns:
            failover_update_returns
        """
        ...
    @typing.overload
    def upgrade(self, 
        _failover_upgrade:'FailoverUpgrade',
    /) -> 'bool': 
        """
        Upgrades both controllers.
        
        Files will be downloaded to the Active Controller and then transferred to the Standby
        Controller.
        
        Upgrade process will start concurrently on both nodes.
        
        Once both upgrades are applied, the Standby Controller will reboot. This job will wait for
        that job to complete before finalizing.
        
        `resume` should be set to `true` if a previous call to this method returned a `CallError` with `errno=EAGAIN`
        meaning that an upgrade can be performed with a warning and that warning is accepted. In that case, you also
        have to set `resume_manual` to `true` if a previous call to this method was performed using update file upload.

        Parameters
        ----------
        failover_upgrade:
            failover_upgrade
        Returns
        -------
        bool:
            upgrade
        """
        ...
    @typing.overload
    def upgrade_finish(self, 
    /) -> 'bool': 
        """
        Perform the last stage of an HA upgrade.
        
        This will activate the new boot environment on the
        Standby Controller and reboot it.

        Parameters
        ----------
        Returns
        -------
        bool:
            upgrade_finish
        """
        ...
    @typing.overload
    def upgrade_pending(self, 
    /) -> 'bool': 
        """
        Verify if HA upgrade is pending.
        
        `upgrade_finish` needs to be called to finish
        the HA upgrade process if this method returns true.

        Parameters
        ----------
        Returns
        -------
        bool:
            upgrade_pending
        """
        ...
    class Action(str,Enum):
        ENABLE = 'ENABLE'
        DISABLE = 'DISABLE'
        ...
    DatasetKeys = typing.TypedDict('DatasetKeys', {
            'name':'str',
            'passphrase':'str',
    })
    FailoverEntry = typing.TypedDict('FailoverEntry', {
            'id':'int',
            'disabled':'bool',
            'timeout':'int',
            'master':'bool',
    })
    FailoverUpdate = typing.TypedDict('FailoverUpdate', {
            'disabled':'bool',
            'timeout':'int',
            'master':'typing.Optional[bool]',
    })
    FailoverUpdateReturns = typing.TypedDict('FailoverUpdateReturns', {
            'id':'int',
            'disabled':'bool',
            'timeout':'int',
            'master':'bool',
    })
    FailoverUpgrade = typing.TypedDict('FailoverUpgrade', {
            'train':'str',
            'resume':'bool',
            'resume_manual':'bool',
    })
    Options = typing.TypedDict('Options', {
            'timeout':'int',
            'job':'bool',
            'job_return':'typing.Optional[bool]',
            'callback':'typing.Union[str, int, bool, dict[str], list]',
            'connect_timeout':'float',
            'raise_connect_error':'bool',
    })
    Options_ = typing.TypedDict('Options_', {
            'active':'bool',
    })
    Options__ = typing.TypedDict('Options__', {
            'reboot':'bool',
    })
    Options___ = typing.TypedDict('Options___', {
            'pools':'list[PoolKeys]',
            'datasets':'list[DatasetKeys]',
    })
    PoolKeys = typing.TypedDict('PoolKeys', {
            'name':'str',
            'passphrase':'str',
    })
