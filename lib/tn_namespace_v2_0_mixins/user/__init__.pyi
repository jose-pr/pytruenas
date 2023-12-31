
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin
from enum import Enum
import typing
class User(
    TableExtMixin,
    Namespace
    ):
    _namespace:typing.Literal['user']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        _user_create:'UserCreate',
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
    @typing.overload
    def delete(self, 
        _id:'int',
        _options:'Options',
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
    @typing.overload
    def get_instance(self, 
        _id:'typing.Union[str, int, bool, dict[str], list]',
        _query_options_get_instance:'QueryOptionsGetInstance',
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
    @typing.overload
    def get_user_obj(self, 
        _get_user_obj:'GetUserObj',
    /) -> 'UserInformation': 
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
        UserInformation:
            user_information
        """
        ...
    @typing.overload
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
    @typing.overload
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
    @typing.overload
    def provisioning_uri(self, 
        _username:'str',
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
    @typing.overload
    def query(self, 
        _query_filters:'list[list]',
        _query_options:'QueryOptions',
    /) -> 'typing.Union[list[UserEntry], UserEntry, int]': 
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
        typing.Union[list[UserEntry], UserEntry, int]:
            
        """
        ...
    @typing.overload
    def renew_2fa_secret(self, 
        _username:'str',
    /) -> 'UserEntry': 
        """
        Renew `username` user's two-factor authentication secret.

        Parameters
        ----------
        username:
            username
        Returns
        -------
        UserEntry:
            user_entry
        """
        ...
    @typing.overload
    def set_root_password(self, 
        _password:'str',
        _options,
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
    @typing.overload
    def setup_local_administrator(self, 
        _username:'Username',
        _password:'str',
        _options:'Options_',
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
    @typing.overload
    def shell_choices(self, 
        _group_ids:'list[int]',
    /) -> 'ShellInfo': 
        """
        Return the available shell choices to be used in `user.create` and `user.update`.
        
        `group_ids` is a list of local group IDs for the user.

        Parameters
        ----------
        group_ids:
            group_ids
        Returns
        -------
        ShellInfo:
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
    @typing.overload
    def unset_2fa_secret(self, 
        _username:'str',
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
    @typing.overload
    def update(self, 
        _id:'int',
        _user_update:'UserUpdate',
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
    @typing.overload
    def verify_twofactor_token(self, 
        _username:'str',
        _token:'typing.Optional[str]',
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
    Ec2 = typing.TypedDict('Ec2', {
            'instance_id':'str',
    })
    GetUserObj = typing.TypedDict('GetUserObj', {
            'username':'str',
            'uid':'int',
            'get_groups':'bool',
            'sid_info':'bool',
    })
    Options = typing.TypedDict('Options', {
            'delete_group':'bool',
    })
    Options_ = typing.TypedDict('Options_', {
            'ec2':'Ec2',
    })
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    ShellInfo = typing.TypedDict('ShellInfo', {
            'shell_path':'str',
    })
    UserCreate = typing.TypedDict('UserCreate', {
            'uid':'int',
            'username':'str',
            'group':'int',
            'group_create':'bool',
            'home':'str',
            'home_mode':'str',
            'home_create':'bool',
            'shell':'str',
            'full_name':'str',
            'email':'typing.Optional[str]',
            'password':'str',
            'password_disabled':'bool',
            'ssh_password_enabled':'bool',
            'locked':'bool',
            'smb':'bool',
            'sudo_commands':'list[str]',
            'sudo_commands_nopasswd':'list[str]',
            'sshpubkey':'typing.Optional[str]',
            'groups':'list[int]',
    })
    UserEntry = typing.TypedDict('UserEntry', {
            'uid':'int',
            'username':'str',
            'home':'str',
            'shell':'str',
            'full_name':'str',
            'email':'typing.Optional[str]',
            'password_disabled':'bool',
            'ssh_password_enabled':'bool',
            'locked':'bool',
            'smb':'bool',
            'sudo_commands':'list[str]',
            'sudo_commands_nopasswd':'list[str]',
            'sshpubkey':'typing.Optional[str]',
            'groups':'list[int]',
            'group':'dict[str]',
            'id':'int',
            'builtin':'bool',
            'id_type_both':'bool',
            'local':'bool',
            'twofactor_auth_configured':'bool',
            'unixhash':'str',
            'smbhash':'str',
            'nt_name':'typing.Optional[str]',
            'sid':'typing.Optional[str]',
    })
    UserInformation = typing.TypedDict('UserInformation', {
            'pw_name':'str',
            'pw_gecos':'str',
            'pw_dir':'str',
            'pw_shell':'str',
            'pw_uid':'int',
            'pw_gid':'int',
            'grouplist':'list',
            'sid_info':'dict[str]',
    })
    UserUpdate = typing.TypedDict('UserUpdate', {
            'uid':'int',
            'username':'str',
            'group':'int',
            'home':'str',
            'home_mode':'str',
            'home_create':'bool',
            'shell':'str',
            'full_name':'str',
            'email':'typing.Optional[str]',
            'password':'str',
            'password_disabled':'bool',
            'ssh_password_enabled':'bool',
            'locked':'bool',
            'smb':'bool',
            'sudo_commands':'list[str]',
            'sudo_commands_nopasswd':'list[str]',
            'sshpubkey':'typing.Optional[str]',
            'groups':'list[int]',
    })
    class Username(str,Enum):
        Root = 'root'
        Admin = 'admin'
        ...
