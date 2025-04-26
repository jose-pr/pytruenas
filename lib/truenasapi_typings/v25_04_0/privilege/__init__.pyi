from pytruenas import Namespace as _NS
import typing as _ty 
class Privilege(_NS):
    
    def create(self,
        privilege_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
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
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PrivilegeDelete:
        """Delete the privilege `id`."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PrivilegeGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PrivilegeQuery:
        """"""
        ...
    def roles(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
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
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PrivilegeUpdate:
        """Update the privilege `id`."""
        ...
class PrivilegeCreate(_ty.TypedDict):
    ...
class PrivilegeDelete(_ty.TypedDict):
    ...
class PrivilegeGet_instance(_ty.TypedDict):
    ...
class PrivilegeQuery(_ty.TypedDict):
    ...
class PrivilegeRoles(_ty.TypedDict):
    ...
class PrivilegeUpdate(_ty.TypedDict):
    ... 