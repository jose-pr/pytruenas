
from pytruenas import Namespace, TrueNASClient
import typing
class Auth(Namespace):
    _namespace:typing.Literal['auth']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def check_password(self, 
        username:'str',
        password:'str',
    /) -> 'bool': 
        """
        Verify username and password

        Parameters
        ----------
        username:
            username
        password:
            password
        Returns
        -------
        bool:
            Is `true` if `username` was successfully validated with provided `password`
        """
        ...
    @typing.overload
    def check_user(self, 
        username:'str',
        password:'str',
    /) -> 'bool': 
        """
        Verify username and password

        Parameters
        ----------
        username:
            username
        password:
            password
        Returns
        -------
        bool:
            Is `true` if `username` was successfully validated with provided `password`
        """
        ...
    @typing.overload
    def generate_token(self, 
        ttl:'int|None'=600,
        attrs:'dict[str]'={},
        match_origin:'bool'=False,
    /) -> 'str': 
        """
        Generate a token to be used for authentication.
        
        `ttl` stands for Time To Live, in seconds. The token will be invalidated if the connection
        has been inactive for a time greater than this.
        
        `attrs` is a general purpose object/dictionary to hold information about the token.
        
        `match_origin` will only allow using this token from the same IP address or with the same user UID.

        Parameters
        ----------
        ttl:
            `ttl` stands for Time To Live, in seconds. The token will be invalidated if the connection
            has been inactive for a time greater than this.
        attrs:
            `attrs` is a general purpose object/dictionary to hold information about the token.
        match_origin:
            match_origin
        Returns
        -------
        str:
            token
        """
        ...
    @typing.overload
    def login(self, 
        username:'str',
        password:'str',
        otp_token:'str|None'=None,
    /) -> 'bool': 
        """
        Authenticate session using username and password.
        `otp_token` must be specified if two factor authentication is enabled.

        Parameters
        ----------
        username:
            username
        password:
            password
        otp_token:
            otp_token
        Returns
        -------
        bool:
            successful_login
        """
        ...
    @typing.overload
    def login_with_api_key(self, 
        api_key:'str',
    /) -> 'bool': 
        """
        Authenticate session using API Key.

        Parameters
        ----------
        api_key:
            api_key
        Returns
        -------
        bool:
            successful_login
        """
        ...
    @typing.overload
    def login_with_token(self, 
        token:'str',
    /) -> 'bool': 
        """
        Authenticate session using token generated with `auth.generate_token`.

        Parameters
        ----------
        token:
            token
        Returns
        -------
        bool:
            successful_login
        """
        ...
    @typing.overload
    def logout(self, 
    /) -> 'bool': 
        """
        Deauthenticates an app and if a token exists, removes that from the
        session.

        Parameters
        ----------
        Returns
        -------
        bool:
            successful_logout
        """
        ...
    @typing.overload
    def me(self, 
    /) -> 'CurrentUserInformation': 
        """
        Returns currently logged-in user.

        Parameters
        ----------
        Returns
        -------
        CurrentUserInformation:
            current_user_information
        """
        ...
    @typing.overload
    def sessions(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'int|Session|list[Session]': 
        """
        Returns list of active auth sessions.
        
        Example of return value:
        
        [
            {
                "id": "NyhB1J5vjPjIV82yZ6caU12HLA1boDJcZNWuVQM4hQWuiyUWMGZTz2ElDp7Yk87d",
                "origin": "192.168.0.3:40392",
                "credentials": "LOGIN_PASSWORD",
                "credentials_data": {"username": "root"},
                "current": True,
                "internal": False,
                "created_at": {"$date": 1545842426070}
            }
        ]
        
        `credentials` can be `UNIX_SOCKET`, `ROOT_TCP_SOCKET`, `LOGIN_PASSWORD`, `API_KEY` or `TOKEN`,
        depending on what authentication method was used.
        For `UNIX_SOCKET` and `LOGIN_PASSWORD` logged-in `username` field will be provided in `credentials_data`.
        For `API_KEY` corresponding `api_key` will be provided in `credentials_data`.
        For `TOKEN` its `parent` credential will be provided in `credentials_data`.
        
        If you want to exclude all internal connections from the list, call this method with following arguments:
        
        [
            [
                ["internal", "=", True]
            ]
        ]

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        int:
            
        Session:
            
        list[Session]:
            
        """
        ...
    @typing.overload
    def set_attribute(self, 
        key:'str',
        value:'str|int|bool|dict[str]|list',
    /) -> None: 
        """
        Set current user's `attributes` dictionary `key` to `value`.
        
        e.g. Setting key="foo" value="var" will result in {"attributes": {"foo": "bar"}}

        Parameters
        ----------
        key:
            Set current user's `attributes` dictionary `key` to `value`.
        value:
            Set current user's `attributes` dictionary `key` to `value`.
        Returns
        -------
        """
        ...
    @typing.overload
    def terminate_other_sessions(self, 
    /) -> None: 
        """
        Terminates all other sessions (except the current one).

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def terminate_session(self, 
        id:'str',
    /) -> 'bool': 
        """
        Terminates session `id`.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        bool:
            Is `true` if session was terminated successfully
        """
        ...
    @typing.overload
    def two_factor_auth(self, 
        username:'str',
        password:'str',
    /) -> 'bool': 
        """
        Returns true if two-factor authorization is required for authorizing user's login.

        Parameters
        ----------
        username:
            username
        password:
            password
        Returns
        -------
        bool:
            Is `true` if 2FA is enabled
        """
        ...

class CurrentUserInformation(typing.TypedDict):
        pw_name:'str'
        pw_gecos:'str'
        pw_dir:'str'
        pw_shell:'str'
        pw_uid:'int'
        pw_gid:'int'
        grouplist:'list'
        sid_info:'dict[str]'
        attributes:'dict[str]'
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
class Session(typing.TypedDict):
        id:'str'
        current:'bool'
        internal:'bool'
        origin:'str'
        credentials:'str'
        created_at:'str'
        ...
