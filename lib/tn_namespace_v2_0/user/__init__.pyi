
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class User(Namespace):
    _namespace:_ty.Literal['user']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        user_create:'dict[str]'={},
    /) -> 'int': 
        """
        Create a new user.
        
        If `uid` is not provided it is automatically filled with the next one available.
        
        `group` is required if `group_create` is false.
        
        `password` is required if `password_disabled` is false.
        
        Available choices for `shell` can be retrieved with `user.shell_choices`.
        
        `smb` specifies whether the user should be allowed access to SMB shares. User
        will also automatically be added to the `builtin_users` group.

        Parameters
        ----------
        user_create:
            user_create
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
        Delete user `id`.
        
        The `delete_group` option deletes the user primary group if it is not being used by
        any other user.

        Parameters
        ----------
        id:
            Delete user `id`.
        options:
            options
        Returns
        -------
        int:
            primary_key
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
    def get_next_uid(self, 
    /) -> 'int': 
        """
        Get the next available/free uid.

        Parameters
        ----------
        Returns
        -------
        int:
            next_available_uid
        """
        ...
    @_ty.overload
    def get_user_obj(self, 
        get_user_obj:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Returns dictionary containing information from struct passwd for the user specified by either
        the username or uid. Bypasses user cache.
        
        Supports the following additional parameters:
        `get_groups` - retrieve group list for the specified user.
        
        NOTE: results will not include nested groups for Active Directory users
        
        `sid_info` - retrieve SID and domain information for the user
        
        NOTE: in some pathological scenarios this may make the operation hang until
        the winbindd request timeout has been reached if the winbindd connection manager
        has not yet marked the domain as offline. The TrueNAS middleware is more aggressive
        about marking AD domains as FAULTED and so it may be advisable to first check the
        Active Directory service state prior to batch operations using this option.

        Parameters
        ----------
        get_user_obj:
            get_user_obj
        Returns
        -------
        dict[str]:
            user_information
        """
        ...
    @_ty.overload
    def has_local_administrator_set_up(self, 
    /) -> 'bool': 
        """
        Return whether a local administrator with a valid password exists.
        
        This is used when the system is installed without a password and must be set on
        first use/login.

        Parameters
        ----------
        Returns
        -------
        bool:
            has_local_administrator_set_up
        """
        ...
    @_ty.overload
    def has_root_password(self, 
    /) -> 'bool': 
        """
        Deprecated method. Use `user.has_local_administrator_set_up`

        Parameters
        ----------
        Returns
        -------
        bool:
            has_root_password
        """
        ...
    @_ty.overload
    def provisioning_uri(self, 
        username:'str',
    /) -> 'str': 
        """
        Returns the provisioning URI for the OTP for `username`. This can then be encoded in a QR code and used
        to provision an OTP app like Google Authenticator.

        Parameters
        ----------
        username:
            username
        Returns
        -------
        str:
            Provisioning URI
        """
        ...
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
        """
        Query users with `query-filters` and `query-options`. As a performance optimization, only local users
        will be queried by default.
        
        Expanded information may be requested by specifying the extra option
        `"extra": {"additional_information": []}`.
        
        The following `additional_information` options are supported:
        `SMB` - include Windows SID and NT Name for user. If this option is not specified, then these
            keys will have `null` value.
        `DS` - include users from Directory Service (LDAP or Active Directory) in results
        
        `"extra": {"search_dscache": true}` is a legacy method of querying for directory services users.

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
    def renew_2fa_secret(self, 
        username:'str',
    /) -> 'dict[str]': 
        """
        Renew `username` user's two-factor authentication secret.

        Parameters
        ----------
        username:
            username
        Returns
        -------
        dict[str]:
            user_entry
        """
        ...
    @_ty.overload
    def set_root_password(self, 
        password:'str',
        options:'dict[str]'={},
    /) -> None: 
        """
        Deprecated method. Use `user.setup_local_administrator`

        Parameters
        ----------
        password:
            password
        options:
            options
        Returns
        -------
        """
        ...
    @_ty.overload
    def setup_local_administrator(self, 
        username:'str',
        password:'str',
        options:'dict[str]'={},
    /) -> None: 
        """
        Set up local administrator (this method does not require authentication if local administrator is not already
        set up).

        Parameters
        ----------
        username:
            username
        password:
            password
        options:
            options
        Returns
        -------
        """
        ...
    @_ty.overload
    def shell_choices(self, 
        group_ids:'list'=[],
    /) -> 'dict[str]': 
        """
        Return the available shell choices to be used in `user.create` and `user.update`.
        
        `group_ids` is a list of local group IDs for the user.

        Parameters
        ----------
        group_ids:
            group_ids
        Returns
        -------
        dict[str]:
            Example(s):
            ```
            {
                "/usr/bin/bash": "bash",
                "/usr/bin/rbash": "rbash",
                "/usr/bin/dash": "dash",
                "/usr/bin/sh": "sh",
                "/usr/bin/zsh": "zsh",
                "/usr/bin/tmux": "tmux",
                "/usr/sbin/nologin": "nologin"
            }
            ```
        """
        ...
    @_ty.overload
    def unset_2fa_secret(self, 
        username:'str',
    /) -> None: 
        """
        Unset two-factor authentication secret for `username`.

        Parameters
        ----------
        username:
            username
        Returns
        -------
        """
        ...
    @_ty.overload
    def update(self, 
        id:'int',
        user_update:'dict[str]'={},
    /) -> 'int': 
        """
        Update attributes of an existing user.

        Parameters
        ----------
        id:
            id
        user_update:
            user_update
        Returns
        -------
        int:
            primary_key
        """
        ...
    @_ty.overload
    def verify_twofactor_token(self, 
        username:'str',
        token:'str|None',
    /) -> 'bool': 
        """
        Returns boolean true if provided `token` is successfully authenticated for `username`.

        Parameters
        ----------
        username:
            username
        token:
            token
        Returns
        -------
        bool:
            token_verified
        """
        ...
