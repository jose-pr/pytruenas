from pytruenas import Namespace as _NS 
class User(_NS):
    
    def create(
        user_create,
    ) -> UserCreate:
        """Create a new user."""
        ...
    def delete(
        id,
        options,
    ) -> UserDelete:
        """Delete user `id`.

The `delete_group` option deletes the user primary group if it is not being used by any other user."""
        ...
    def get_instance(
        id,
        options,
    ) -> UserGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def get_next_uid(
    ) -> UserGet_next_uid:
        """Get the next available/free uid."""
        ...
    def get_user_obj(
        get_user_obj,
    ) -> UserGet_user_obj:
        """Returns dictionary containing information from struct passwd for the user specified by either the username or uid. Bypasses user cache.

NOTE: results will not include nested groups for Active Directory users."""
        ...
    def has_local_administrator_set_up(
    ) -> UserHas_local_administrator_set_up:
        """Return whether a local administrator with a valid password exists.

This is used when the system is installed without a password and must be set on first use/login."""
        ...
    def query(
        filters,
        options,
    ) -> UserQuery:
        """Query users with `query-filters` and `query-options`.

If users provided by Active Directory or LDAP are not desired, then "local", "=", True should be added to filters."""
        ...
    def renew_2fa_secret(
        username,
        twofactor_options,
    ) -> UserRenew_2fa_secret:
        """Renew `username` user's two-factor authentication secret.

NOTE: This username must match the authenticated username unless authenticated credentials have FULL_ADMIN role."""
        ...
    def set_password(
        set_password_data,
    ) -> UserSet_password:
        """Set the password of the specified `username` to the `new_password` specified in payload.

ValidationErrors will be raised in the following situations: * username does not exist * account is not local to the NAS (Active Directory, LDAP, etc) * account has password authentication disabled * account is locked

NOTE: when authenticated session has less than FULL_ADMIN role, password changes will be rejected if the payload does not match the currently-authenticated user.

NOTE: users authenticated with a one-time password will be able to change the password without submitting a second time."""
        ...
    def setup_local_administrator(
        username,
        password,
        options,
    ) -> UserSetup_local_administrator:
        """Set up local administrator (this method does not require authentication if local administrator is not already set up)."""
        ...
    def shell_choices(
        group_ids,
    ) -> UserShell_choices:
        """Return the available shell choices to be used in `user.create` and `user.update`.

`group_ids` is a list of local group IDs for the user."""
        ...
    def unset_2fa_secret(
        username,
    ) -> UserUnset_2fa_secret:
        """Unset two-factor authentication secret for `username`."""
        ...
    def update(
        id,
        user_update,
    ) -> UserUpdate:
        """Update attributes of an existing user."""
        ...
class UserCreate:
    ...
class UserDelete:
    ...
class UserGet_instance:
    ...
class UserGet_next_uid:
    ...
class UserGet_user_obj:
    ...
class UserHas_local_administrator_set_up:
    ...
class UserQuery:
    ...
class UserRenew_2fa_secret:
    ...
class UserSet_password:
    ...
class UserSetup_local_administrator:
    ...
class UserShell_choices:
    ...
class UserUnset_2fa_secret:
    ...
class UserUpdate:
    ... 