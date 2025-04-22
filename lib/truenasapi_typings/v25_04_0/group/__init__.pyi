from pytruenas import Namespace as _NS 
class Group(_NS):
    
    def create(self,
        group_create,
    ) -> GroupCreate:
        """Create a new group."""
        ...
    def delete(self,
        id,
        options,
    ) -> GroupDelete:
        """Delete group `id`.

The `delete_users` option deletes all users that have this group as their primary group."""
        ...
    def get_group_obj(self,
        get_group_obj,
    ) -> GroupGet_group_obj:
        """Returns dictionary containing information from struct grp for the group specified by either the `groupname` or `gid`.

If `sid_info` is specified then addition SMB / domain information is returned for the group."""
        ...
    def get_instance(self,
        id,
        options,
    ) -> GroupGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def get_next_gid(self,
    ) -> GroupGet_next_gid:
        """Get the next available/free gid."""
        ...
    def has_password_enabled_user(self,
        gids,
        exclude_user_ids,
    ) -> GroupHas_password_enabled_user:
        """Checks whether at least one local user with a password is a member of any of the `group_ids`."""
        ...
    def query(self,
        filters,
        options,
    ) -> GroupQuery:
        """Query groups with `query-filters` and `query-options`."""
        ...
    def update(self,
        id,
        group_update,
    ) -> GroupUpdate:
        """Update attributes of an existing group."""
        ...
class GroupCreate:
    ...
class GroupDelete:
    ...
class GroupGet_group_obj:
    ...
class GroupGet_instance:
    ...
class GroupGet_next_gid:
    ...
class GroupHas_password_enabled_user:
    ...
class GroupQuery:
    ...
class GroupUpdate:
    ... 