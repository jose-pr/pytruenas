
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Group(Namespace):
    _namespace:_ty.Literal['group']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        group_create:'dict[str]'={},
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
    @_ty.overload
    def delete(self, 
        id:'int',
        options:'dict[str]'={},
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
    @_ty.overload
    def get_group_obj(self, 
        get_group_obj:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Returns dictionary containing information from struct grp for the group specified by either
        the groupname or gid. Bypasses group cache.

        Parameters
        ----------
        get_group_obj:
            get_group_obj
        Returns
        -------
        dict[str]:
            group_info
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
    @_ty.overload
    def has_password_enabled_user(self, 
        gids:'list'=[],
        exclude_user_ids:'list'=[],
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
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
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
        list:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @_ty.overload
    def update(self, 
        id:'int',
        group_update:'dict[str]'={},
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
