from pytruenas import Namespace as _NS
import typing as _ty 
class User(_NS):
    
    def create(self,
        user_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UserCreate:
        """Create a new user."""
        ...
    def delete(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UserDelete:
        """Delete user `id`.

The `delete_group` option deletes the user primary group if it is not being used by any other user."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UserGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def get_next_uid(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UserGet_next_uid:
        """Get the next available/free uid."""
        ...
    def get_user_obj(self,
        get_user_obj,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UserGet_user_obj:
        """Returns dictionary containing information from struct passwd for the user specified by either the username or uid. Bypasses user cache.

NOTE: results will not include nested groups for Active Directory users."""
        ...
    def has_local_administrator_set_up(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UserHas_local_administrator_set_up:
        """Return whether a local administrator with a valid password exists.

This is used when the system is installed without a password and must be set on first use/login."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UserQuery:
        """Query users with `query-filters` and `query-options`.

If users provided by Active Directory or LDAP are not desired, then "local", "=", True should be added to filters."""
        ...
    def renew_2fa_secret(self,
        username,
        twofactor_options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UserRenew_2fa_secret:
        """Renew `username` user's two-factor authentication secret.

NOTE: This username must match the authenticated username unless authenticated credentials have FULL_ADMIN role."""
        ...
    def set_password(self,
        set_password_data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UserSet_password:
        """Set the password of the specified `username` to the `new_password` specified in payload.

ValidationErrors will be raised in the following situations: * username does not exist * account is not local to the NAS (Active Directory, LDAP, etc) * account has password authentication disabled * account is locked

NOTE: when authenticated session has less than FULL_ADMIN role, password changes will be rejected if the payload does not match the currently-authenticated user.

NOTE: users authenticated with a one-time password will be able to change the password without submitting a second time."""
        ...
    def setup_local_administrator(self,
        username,
        password,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UserSetup_local_administrator:
        """Set up local administrator (this method does not require authentication if local administrator is not already set up)."""
        ...
    def shell_choices(self,
        group_ids,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UserShell_choices:
        """Return the available shell choices to be used in `user.create` and `user.update`.

`group_ids` is a list of local group IDs for the user."""
        ...
    def unset_2fa_secret(self,
        username,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UserUnset_2fa_secret:
        """Unset two-factor authentication secret for `username`."""
        ...
    def update(self,
        id,
        user_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UserUpdate:
        """Update attributes of an existing user."""
        ...
class UserCreate(_ty.TypedDict):
    ...
class UserDelete(_ty.TypedDict):
    ...
class UserGet_instance(_ty.TypedDict):
    ...
class UserGet_next_uid(_ty.TypedDict):
    ...
class UserGet_user_obj(_ty.TypedDict):
    ...
class UserHas_local_administrator_set_up(_ty.TypedDict):
    ...
class UserQuery(_ty.TypedDict):
    ...
class UserRenew_2fa_secret(_ty.TypedDict):
    ...
class UserSet_password(_ty.TypedDict):
    ...
class UserSetup_local_administrator(_ty.TypedDict):
    ...
class UserShell_choices(_ty.TypedDict):
    ...
class UserUnset_2fa_secret(_ty.TypedDict):
    ...
class UserUpdate(_ty.TypedDict):
    ... 