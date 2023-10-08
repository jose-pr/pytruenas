
from pytruenas import Namespace, TrueNASClient
import typing
class Privilege(Namespace):
    _namespace:typing.Literal['privilege']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        privilege_create:'PrivilegeCreate'={},
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
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'QueryOptionsGetInstance'={},
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
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'list[PrivilegeEntry]|PrivilegeEntry|int|PrivilegeEntry': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list[PrivilegeEntry]:
            
        PrivilegeEntry:
            
        int:
            
        PrivilegeEntry:
            
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        privilege_update:'PrivilegeUpdate'={},
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

class PrivilegeCreate(typing.TypedDict):
        id:'int'
        name:'str'
        local_groups:'list[int]'
        ds_groups:'list[typing.Union[int, str]]'
        allowlist:'list[AllowlistItem]'
        roles:'list[str]'
        web_shell:'bool'
        ...
class AllowlistItem(typing.TypedDict):
        method:'str'
        resource:'str'
        ...
class PrivilegeCreateReturns(typing.TypedDict):
        id:'int'
        builtin_name:'typing.Optional[str]'
        name:'str'
        local_groups:'list[int]'
        ds_groups:'list[typing.Union[int, str]]'
        allowlist:'list[AllowlistItem]'
        roles:'list[str]'
        web_shell:'bool'
        ...
class QueryOptionsGetInstance(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class QueryOptions(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class PrivilegeEntry(typing.TypedDict):
        id:'int'
        builtin_name:'typing.Optional[str]'
        name:'str'
        local_groups:'list[int]'
        ds_groups:'list[typing.Union[int, str]]'
        allowlist:'list[AllowlistItem]'
        roles:'list[str]'
        web_shell:'bool'
        ...
class PrivilegeUpdate(typing.TypedDict):
        id:'int'
        name:'str'
        local_groups:'list[int]'
        ds_groups:'list[typing.Union[int, str]]'
        allowlist:'list[AllowlistItem]'
        roles:'list[str]'
        web_shell:'bool'
        ...
class PrivilegeUpdateReturns(typing.TypedDict):
        id:'int'
        builtin_name:'typing.Optional[str]'
        name:'str'
        local_groups:'list[int]'
        ds_groups:'list[typing.Union[int, str]]'
        allowlist:'list[AllowlistItem]'
        roles:'list[str]'
        web_shell:'bool'
        ...
