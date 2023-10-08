
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Rsynctask(Namespace):
    _namespace:_ty.Literal['rsynctask']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        rsync_task_create:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            rsynctask_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
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
    def run(self, 
        id:'int',
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
    @_ty.overload
    def update(self, 
        id:'int',
        rsync_task_update:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            rsynctask_update_returns
        """
        ...
