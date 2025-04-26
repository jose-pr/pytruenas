from pytruenas import Namespace as _NS
import typing as _ty 
class Group(_NS):
    
    def create(self,
        group_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GroupCreate:
        """Create a new group."""
        ...
    def delete(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GroupDelete:
        """Delete group `id`.

The `delete_users` option deletes all users that have this group as their primary group."""
        ...
    def get_group_obj(self,
        get_group_obj,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GroupGet_group_obj:
        """Returns dictionary containing information from struct grp for the group specified by either the `groupname` or `gid`.

If `sid_info` is specified then addition SMB / domain information is returned for the group."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GroupGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def get_next_gid(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GroupGet_next_gid:
        """Get the next available/free gid."""
        ...
    def has_password_enabled_user(self,
        gids,
        exclude_user_ids,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GroupHas_password_enabled_user:
        """Checks whether at least one local user with a password is a member of any of the `group_ids`."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GroupQuery:
        """Query groups with `query-filters` and `query-options`."""
        ...
    def update(self,
        id,
        group_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GroupUpdate:
        """Update attributes of an existing group."""
        ...
class GroupCreate(_ty.TypedDict):
    ...
class GroupDelete(_ty.TypedDict):
    ...
class GroupGet_group_obj(_ty.TypedDict):
    ...
class GroupGet_instance(_ty.TypedDict):
    ...
class GroupGet_next_gid(_ty.TypedDict):
    ...
class GroupHas_password_enabled_user(_ty.TypedDict):
    ...
class GroupQuery(_ty.TypedDict):
    ...
class GroupUpdate(_ty.TypedDict):
    ... 