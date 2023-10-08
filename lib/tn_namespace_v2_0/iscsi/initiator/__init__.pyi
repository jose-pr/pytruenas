
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class IscsiInitiator(Namespace):
    _namespace:_ty.Literal['iscsi.initiator']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        iscsi_initiator_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create an iSCSI Initiator.
        
        `initiators` is a list of initiator hostnames which are authorized to access an iSCSI Target. To allow all
        possible initiators, `initiators` can be left empty.

        Parameters
        ----------
        iscsi_initiator_create:
            iscsi_initiator_create
        Returns
        -------
        dict[str]:
            iscsi_initiator_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete iSCSI initiator of `id`.

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
    def update(self, 
        id:'int',
        iscsi_initiator_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update iSCSI initiator of `id`.

        Parameters
        ----------
        id:
            Update iSCSI initiator of `id`.
            Create an iSCSI Initiator.
        iscsi_initiator_update:
            iscsi_initiator_update
        Returns
        -------
        dict[str]:
            iscsi_initiator_update_returns
        """
        ...
