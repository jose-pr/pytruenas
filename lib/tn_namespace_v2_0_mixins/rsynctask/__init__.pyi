
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin
from enum import Enum
import typing
class Rsynctask(
    TableExtMixin,
    Namespace
    ):
    _namespace:typing.Literal['rsynctask']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        _rsync_task_create:'RsyncTaskCreate',
    /) -> 'RsynctaskCreateReturns': 
        """
        Create a Rsync Task.
        
        See the comment in Rsyncmod about `path` length limits.
        
        `remotehost` is ip address or hostname of the remote system. If username differs on the remote host,
        "username@remote_host" format should be used.
        
        `mode` represents different operating mechanisms for Rsync i.e Rsync Module mode / Rsync SSH mode.
        
        In SSH mode, if `ssh_credentials` (a keychain credential of `SSH_CREDENTIALS` type) is specified then it is used
        to connect to the remote host. If it is not specified, then keys in `user`'s .ssh directory are used.
        `remotehost` and `remoteport` are not used in this case.
        
        `remotemodule` is the name of remote module, this attribute should be specified when `mode` is set to MODULE.
        
        `remotepath` specifies the path on the remote system.
        
        `validate_rpath` is a boolean which when sets validates the existence of the remote path.
        
        `ssh_keyscan` will automatically add remote host key to user's known_hosts file.
        
        `direction` specifies if data should be PULLED or PUSHED from the remote system.
        
        `compress` when set reduces the size of the data which is to be transmitted.
        
        `archive` when set makes rsync run recursively, preserving symlinks, permissions, modification times, group,
        and special files.
        
        `delete` when set deletes files in the destination directory which do not exist in the source directory.
        
        `preserveperm` when set preserves original file permissions.

        Parameters
        ----------
        rsync_task_create:
            rsync_task_create
        Returns
        -------
        RsynctaskCreateReturns:
            rsynctask_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        _id:'int',
    /) -> 'bool': 
        """
        Delete Rsync Task of `id`.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
        """
        ...
    @typing.overload
    def get_instance(self, 
        _id:'typing.Union[str, int, bool, dict[str], list]',
        _query_options_get_instance:'QueryOptionsGetInstance',
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
    @typing.overload
    def query(self, 
        _query_filters:'list[list]',
        _query_options:'QueryOptions',
    /) -> 'typing.Union[list[RsyncTaskEntry], RsyncTaskEntry, int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[RsyncTaskEntry], RsyncTaskEntry, int]:
            
        """
        ...
    @typing.overload
    def run(self, 
        _id:'int',
    /) -> None: 
        """
        Job to run rsync task of `id`.
        
        Output is saved to job log excerpt (not syslog).

        Parameters
        ----------
        id:
            Job to run rsync task of `id`.
        Returns
        -------
        """
        ...
    @typing.overload
    def update(self, 
        _id:'int',
        _rsync_task_update:'RsyncTaskUpdate',
    /) -> 'RsynctaskUpdateReturns': 
        """
        Update Rsync Task of `id`.

        Parameters
        ----------
        id:
            Update Rsync Task of `id`.
            Create a Rsync Task.
        rsync_task_update:
            rsync_task_update
        Returns
        -------
        RsynctaskUpdateReturns:
            rsynctask_update_returns
        """
        ...
    class Direction(str,Enum):
        PULL = 'PULL'
        PUSH = 'PUSH'
        ...
    class Mode(str,Enum):
        MODULE = 'MODULE'
        SSH = 'SSH'
        ...
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    RsyncTaskCreate = typing.TypedDict('RsyncTaskCreate', {
            'path':'str',
            'user':'str',
            'mode':'Mode',
            'remotehost':'typing.Optional[str]',
            'remoteport':'typing.Optional[int]',
            'remotemodule':'typing.Optional[str]',
            'ssh_credentials':'typing.Optional[int]',
            'remotepath':'str',
            'validate_rpath':'bool',
            'ssh_keyscan':'bool',
            'direction':'Direction',
            'desc':'str',
            'schedule':'Schedule',
            'recursive':'bool',
            'times':'bool',
            'compress':'bool',
            'archive':'bool',
            'delete':'bool',
            'quiet':'bool',
            'preserveperm':'bool',
            'preserveattr':'bool',
            'delayupdates':'bool',
            'extra':'list[str]',
            'enabled':'bool',
    })
    RsyncTaskEntry = typing.TypedDict('RsyncTaskEntry', {
            'path':'str',
            'user':'str',
            'mode':'Mode',
            'remotehost':'typing.Optional[str]',
            'remoteport':'typing.Optional[int]',
            'remotemodule':'typing.Optional[str]',
            'remotepath':'str',
            'direction':'Direction',
            'desc':'str',
            'schedule':'Schedule',
            'recursive':'bool',
            'times':'bool',
            'compress':'bool',
            'archive':'bool',
            'delete':'bool',
            'quiet':'bool',
            'preserveperm':'bool',
            'preserveattr':'bool',
            'delayupdates':'bool',
            'extra':'list[str]',
            'enabled':'bool',
            'id':'int',
            'ssh_credentials':'dict[str]',
            'locked':'bool',
            'job':'dict[str]',
    })
    RsyncTaskUpdate = typing.TypedDict('RsyncTaskUpdate', {
            'path':'str',
            'user':'str',
            'mode':'Mode',
            'remotehost':'typing.Optional[str]',
            'remoteport':'typing.Optional[int]',
            'remotemodule':'typing.Optional[str]',
            'ssh_credentials':'typing.Optional[int]',
            'remotepath':'str',
            'validate_rpath':'bool',
            'ssh_keyscan':'bool',
            'direction':'Direction',
            'desc':'str',
            'schedule':'Schedule',
            'recursive':'bool',
            'times':'bool',
            'compress':'bool',
            'archive':'bool',
            'delete':'bool',
            'quiet':'bool',
            'preserveperm':'bool',
            'preserveattr':'bool',
            'delayupdates':'bool',
            'extra':'list[str]',
            'enabled':'bool',
    })
    RsynctaskCreateReturns = typing.TypedDict('RsynctaskCreateReturns', {
            'path':'str',
            'user':'str',
            'mode':'Mode',
            'remotehost':'typing.Optional[str]',
            'remoteport':'typing.Optional[int]',
            'remotemodule':'typing.Optional[str]',
            'remotepath':'str',
            'direction':'Direction',
            'desc':'str',
            'schedule':'Schedule',
            'recursive':'bool',
            'times':'bool',
            'compress':'bool',
            'archive':'bool',
            'delete':'bool',
            'quiet':'bool',
            'preserveperm':'bool',
            'preserveattr':'bool',
            'delayupdates':'bool',
            'extra':'list[str]',
            'enabled':'bool',
            'id':'int',
            'ssh_credentials':'dict[str]',
            'locked':'bool',
            'job':'dict[str]',
    })
    RsynctaskUpdateReturns = typing.TypedDict('RsynctaskUpdateReturns', {
            'path':'str',
            'user':'str',
            'mode':'Mode',
            'remotehost':'typing.Optional[str]',
            'remoteport':'typing.Optional[int]',
            'remotemodule':'typing.Optional[str]',
            'remotepath':'str',
            'direction':'Direction',
            'desc':'str',
            'schedule':'Schedule',
            'recursive':'bool',
            'times':'bool',
            'compress':'bool',
            'archive':'bool',
            'delete':'bool',
            'quiet':'bool',
            'preserveperm':'bool',
            'preserveattr':'bool',
            'delayupdates':'bool',
            'extra':'list[str]',
            'enabled':'bool',
            'id':'int',
            'ssh_credentials':'dict[str]',
            'locked':'bool',
            'job':'dict[str]',
    })
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
