
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class IscsiGlobal_(Namespace):
    _namespace:_ty.Literal['iscsi.global']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def alua_enabled(self, 
    /) -> None: 
        """
        Returns whether iSCSI ALUA is enabled or not.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @_ty.overload
    def client_count(self, 
    /) -> None: 
        """
        Return currently connected clients count.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @_ty.overload
    def config(self, 
    /) -> 'dict[str]': 
        """
        

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            iscsi_global_entry
        """
        ...
    @_ty.overload
    def sessions(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'int|dict[str]|list': 
        """
        Get a list of currently running iSCSI sessions. This includes initiator and target names
        and the unique connection IDs.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        int:
            
        dict[str]:
            
        list:
            
        """
        ...
    @_ty.overload
    def update(self, 
        iscsiglobal_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        `alua` is a no-op for FreeNAS.

        Parameters
        ----------
        iscsiglobal_update:
            iscsiglobal_update
        Returns
        -------
        dict[str]:
            iscsi_global_update_returns
        """
        ...
