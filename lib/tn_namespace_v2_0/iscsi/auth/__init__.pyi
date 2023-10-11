
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class IscsiAuth(
    Namespace
    ):
    _namespace:typing.Literal['iscsi.auth']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        iscsi_auth_create:'IscsiAuthCreate',
    /) -> 'dict[str]': 
        """
        Create an iSCSI Authorized Access.
        
        `tag` should be unique among all configured iSCSI Authorized Accesses.
        
        `secret` and `peersecret` should have length between 12-16 letters inclusive.
        
        `peeruser` and `peersecret` are provided only when configuring mutual CHAP. `peersecret` should not be
        similar to `secret`.

        Parameters
        ----------
        iscsi_auth_create:
            iscsi_auth_create
        Returns
        -------
        dict[str]:
            iscsi_auth_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete iSCSI Authorized Access of `id`.

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
        id:'typing.Union[str, int, bool, dict[str], list]',
        query_options_get_instance:'QueryOptionsGetInstance',
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
        query_filters:'list[list]',
        query_options:'QueryOptions',
    /) -> 'typing.Union[list, dict[str], int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list, dict[str], int]:
            
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        iscsi_auth_update:'IscsiAuthUpdate',
    /) -> 'dict[str]': 
        """
        Update iSCSI Authorized Access of `id`.

        Parameters
        ----------
        id:
            Update iSCSI Authorized Access of `id`.
            Create an iSCSI Authorized Access.
        iscsi_auth_update:
            iscsi_auth_update
        Returns
        -------
        dict[str]:
            iscsi_auth_update_returns
        """
        ...
    IscsiAuthCreate = typing.TypedDict('IscsiAuthCreate', {
            'tag':'int',
            'user':'str',
            'secret':'str',
            'peeruser':'str',
            'peersecret':'str',
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
    IscsiAuthUpdate = typing.TypedDict('IscsiAuthUpdate', {
            'tag':'int',
            'user':'str',
            'secret':'str',
            'peeruser':'str',
            'peersecret':'str',
    })
