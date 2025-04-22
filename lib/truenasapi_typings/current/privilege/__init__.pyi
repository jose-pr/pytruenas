from pytruenas import Namespace as _NS 
class Privilege(_NS):
    
    def create(self,
        privilege_create,
    ) -> PrivilegeCreate:
        """Creates a privilege.

`name` is a name for privilege (must be unique).

`local_groups` is a list of local user account group GIDs that gain this privilege.

`ds_groups` is list of Directory Service group GIDs that will gain this privilege.

`roles` is a list of roles to be assigned to the privilege

`web_shell` controls whether users with this privilege are allowed to log in to the Web UI."""
        ...
    def delete(self,
        id,
    ) -> PrivilegeDelete:
        """Delete the privilege `id`."""
        ...
    def get_instance(self,
        id,
        options,
    ) -> PrivilegeGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
    ) -> PrivilegeQuery:
        """"""
        ...
    def roles(self,
        filters,
        options,
    ) -> PrivilegeRoles:
        """Get all available roles.

Each entry contains the following keys:

`name` - the internal name of the role

`includes` - list of other roles that this role includes. When user is granted this role, they will also receive permissions granted by all the included roles.

`builtin` - role exists for internal backend purposes for access control."""
        ...
    def update(self,
        id,
        privilege_update,
    ) -> PrivilegeUpdate:
        """Update the privilege `id`."""
        ...
class PrivilegeCreate:
    ...
class PrivilegeDelete:
    ...
class PrivilegeGet_instance:
    ...
class PrivilegeQuery:
    ...
class PrivilegeRoles:
    ...
class PrivilegeUpdate:
    ... 