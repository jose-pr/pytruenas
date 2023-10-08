
from pytruenas import Namespace, TrueNASClient
import typing
class Group(Namespace):
    _namespace:typing.Literal['group']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        group_create:'GroupCreate'={},
    /) -> 'int': 
        """
        Create a new group.
        
        If `gid` is not provided it is automatically filled with the next one available.
        
        `allow_duplicate_gid` allows distinct group names to share the same gid.
        
        `users` is a list of user ids (`id` attribute from `user.query`).
        
        `smb` specifies whether the group should be mapped into an NT group.

        Parameters
        ----------
        group_create:
            group_create
        Returns
        -------
        int:
            primary_key
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
        options:'Options'={},
    /) -> 'int': 
        """
        Delete group `id`.
        
        The `delete_users` option deletes all users that have this group as their primary group.

        Parameters
        ----------
        id:
            Delete group `id`.
        options:
            options
        Returns
        -------
        int:
            primary_key
        """
        ...
    @typing.overload
    def get_group_obj(self, 
        get_group_obj:'GetGroupObj'={},
    /) -> 'GroupInfo': 
        """
        Returns dictionary containing information from struct grp for the group specified by either
        the groupname or gid. Bypasses group cache.

        Parameters
        ----------
        get_group_obj:
            get_group_obj
        Returns
        -------
        GroupInfo:
            group_info
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
    def get_next_gid(self, 
    /) -> 'int': 
        """
        Get the next available/free gid.

        Parameters
        ----------
        Returns
        -------
        int:
            next_available_gid
        """
        ...
    @typing.overload
    def has_password_enabled_user(self, 
        gids:'list[int]'=[],
        exclude_user_ids:'list[int]'=[],
    /) -> None: 
        """
        Checks whether at least one local user with a password is a member of any of the `group_ids`.

        Parameters
        ----------
        gids:
            gids
        exclude_user_ids:
            exclude_user_ids
        Returns
        -------
        """
        ...
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'list[GroupEntry]|GroupEntry|int|GroupEntry': 
        """
        Query groups with `query-filters` and `query-options`. As a performance optimization, only local groups
        will be queried by default.
        
        Expanded information may be requested by specifying the extra option `"extra": {"additional_information": []}`.
        
        The following `additional_information` options are supported:
        `SMB` - include Windows SID and NT Name for group. If this option is not specified, then these
            keys will have `null` value.
        `DS` - include groups from Directory Service (LDAP or Active Directory) in results
        
        `"extra": {"search_dscache": true}` is a legacy method of querying for directory services groups.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list[GroupEntry]:
            
        GroupEntry:
            
        int:
            
        GroupEntry:
            
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        group_update:'GroupUpdate'={},
    /) -> 'int': 
        """
        Update attributes of an existing group.

        Parameters
        ----------
        id:
            `users` is a list of user ids (`id` attribute from `user.query`).
        group_update:
            group_update
        Returns
        -------
        int:
            primary_key
        """
        ...

class GroupCreate(typing.TypedDict):
        gid:'int'
        name:'str'
        smb:'bool'
        sudo_commands:'list[str]'
        sudo_commands_nopasswd:'list[str]'
        allow_duplicate_gid:'bool'
        users:'list[int]'
        ...
class Options(typing.TypedDict):
        delete_users:'bool'
        ...
class GetGroupObj(typing.TypedDict):
        groupname:'str'
        gid:'int'
        ...
class GroupInfo(typing.TypedDict):
        gr_name:'str'
        gr_gid:'int'
        gr_mem:'list'
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
class GroupEntry(typing.TypedDict):
        gid:'int'
        name:'str'
        smb:'bool'
        sudo_commands:'list[str]'
        sudo_commands_nopasswd:'list[str]'
        users:'list[int]'
        id:'int'
        group:'str'
        builtin:'bool'
        id_type_both:'bool'
        local:'bool'
        nt_name:'typing.Optional[str]'
        sid:'typing.Optional[str]'
        ...
class GroupUpdate(typing.TypedDict):
        gid:'int'
        name:'str'
        smb:'bool'
        sudo_commands:'list[str]'
        sudo_commands_nopasswd:'list[str]'
        allow_duplicate_gid:'bool'
        users:'list[int]'
        ...
