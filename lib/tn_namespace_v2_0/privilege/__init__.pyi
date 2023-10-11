
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Privilege(
    Namespace
    ):
    _namespace:typing.Literal['privilege']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        privilege_create:'PrivilegeCreate',
    /) -> 'PrivilegeCreateReturns': 
        """
        Creates a privilege.
        
        `name` is a name for privilege (must be unique).
        
        `local_groups` is a list of local user account group GIDs that gain this privilege.
        
        `ds_groups` is list of Directory Service group GIDs that will gain this privilege.
        
        `allowlist` is a list of API endpoints allowed for this privilege.
        
        `web_shell` controls whether users with this privilege are allowed to log in to the Web UI.

        Parameters
        ----------
        privilege_create:
            privilege_create
        Returns
        -------
        PrivilegeCreateReturns:
            privilege_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete the privilege `id`.

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
    /) -> 'typing.Union[list[PrivilegeEntry], PrivilegeEntry, int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[PrivilegeEntry], PrivilegeEntry, int]:
            
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        privilege_update:'PrivilegeUpdate',
    /) -> 'PrivilegeUpdateReturns': 
        """
        Update the privilege `id`.

        Parameters
        ----------
        id:
            Update the privilege `id`.
            Creates a privilege.
        privilege_update:
            privilege_update
        Returns
        -------
        PrivilegeUpdateReturns:
            privilege_update_returns
        """
        ...
    PrivilegeCreate = typing.TypedDict('PrivilegeCreate', {
            'id':'int',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[int]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem = typing.TypedDict('AllowlistItem', {
            'method':'Method',
            'resource':'str',
    })
    class Method(str,Enum):
        GET = 'GET'
        POST = 'POST'
        PUT = 'PUT'
        DELETE = 'DELETE'
        CALL = 'CALL'
        SUBSCRIBE = 'SUBSCRIBE'
        All = '*'
        ...
    PrivilegeCreateReturns = typing.TypedDict('PrivilegeCreateReturns', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[int]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
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
    PrivilegeEntry = typing.TypedDict('PrivilegeEntry', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[int]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    PrivilegeUpdate = typing.TypedDict('PrivilegeUpdate', {
            'id':'int',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[int]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    PrivilegeUpdateReturns = typing.TypedDict('PrivilegeUpdateReturns', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[int]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
