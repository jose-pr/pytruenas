from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Auth(_NS):
    
    def generate_onetime_password(self,
        generate_single_use_password:GenerateOnetimePasswordGenerateSingleUsePassword,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> str:
        """Generate a password for the specified username that may be used only a single time to authenticate to TrueNAS. This may be used by server administrators to allow users authenticate and then set a proper password and two-factor authentication token."""
        ...
    def generate_token(self,
        ttl:int|None=600,
        attrs:_jsonschema.JsonObject={},
        match_origin:bool=True,
        single_use:bool=False,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> str:
        """Generate a token to be used for authentication.

`ttl` stands for Time To Live, in seconds. The token will be invalidated if the connection has been inactive for a time greater than this.

`attrs` is a general purpose object/dictionary to hold information about the token.

`match_origin` will only allow using this token from the same IP address or with the same user UID.

NOTE: this endpoint is not supported when server security requires replay-resistant authentication as part of GPOS STIG requirements."""
        ...
    def login(self,
        username:str,
        password:str,
        otp_token:str|None=None,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Authenticate session using username and password. `otp_token` must be specified if two factor authentication is enabled."""
        ...
    def login_ex(self,
        login_data:LoginExAuthApiKeyPlain|LoginExAuthPasswordPlain|LoginExAuthTokenPlain|LoginExAuthOTPToken,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> LoginExAuthRespSuccess|LoginExAuthRespAuthErr|LoginExAuthRespExpired|LoginExAuthRespOTPRequired|LoginExAuthRespAuthRedirect:
        """Authenticate using one of a variety of mechanisms

NOTE: mechanisms with a _PLAIN suffix indicate that they involve passing plain-text passwords or password-equivalent strings and should not be used on untrusted / insecure transport. Available mechanisms will be expanded in future releases.

params: This takes a single argument consistning of a JSON object with the following keys:

    mechanism: the mechanism by which to authenticate to the backend the exact parameters to use vary by mechanism and are described below

    PASSWORD_PLAIN username: username with which to authenticate password: password with which to authenticate login_options: dictionary with additional authentication options

    API_KEY_PLAIN username: username with which to authenticate api_key: API key string login_options: dictionary with additional authentication options

    AUTH_TOKEN_PLAIN token: authentication token string login_options: dictionary with additional authentication options

    OTP_TOKEN otp_token: one-time password token. This is only permitted if a previous auth.login_ex call responded with "OTP_REQUIRED".

    login_options user_info: boolean - include auth.me output in successful responses.

raises: CallError: a middleware CallError may be raised in the following circumstances.

    * An multistep challenge-response authentication mechanism is being used and the specified `mechanism` does not match the expected next step for authentication. In this case the errno will be set to EBUSY.

    * OTP_TOKEN mechanism was passed without an explicit request from a previous authentication step. In this case the errno will be set to EINVAL.

    * Current authenticator assurance level prohibits the use of the specified authentication mechanism. In this case the errno will be set to EOPNOTSUPP.

returns: JSON object containing the following keys:

    response_type: string indicating the results of the current authentication mechanism. This is used to inform client of nature of authentication error or whether further action will be required in order to complete authentication.

    <additional keys per response_type>

Notes about response types:

SUCCESS: additional key: user_info: includes auth.me output for the resulting authenticated credentials.

OTP_REQUIRED additional key: username: normalized username of user who must provide an OTP token.

AUTH_ERR Generic authentication error corresponds to PAM_AUTH_ERR and PAM_USER_UNKOWN from libpam. This may be returned if the account does not exist or if the credential is incorrect.

EXPIRED The specified credential is expired and not suitable for authentication.

REDIRECT Authentication must be performed on different server."""
        ...
    def login_ex_continue(self,
        login_data:LoginExContinueLoginData,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> LoginExContinueAuthRespSuccess|LoginExContinueAuthRespAuthErr|LoginExContinueAuthRespExpired|LoginExContinueAuthRespOTPRequired|LoginExContinueAuthRespAuthRedirect:
        """Continue in-progress authentication attempt. This endpoint should be called to continue an auth.login_ex attempt that returned OTP_REQUIRED.

This is a convenience wrapper around auth.login_ex for API consumers.

params: mechanism: the mechanism by which to continue authentication. Currently the only supported mechanism here is OTP_TOKEN.

    OTP_TOKEN otp_token: one-time password token. This is only permitted if a previous auth.login_ex call responded with "OTP_REQUIRED".

returns: JSON object containing the following keys:

    `response_type` - will be one of the following: SUCCESS - continued auth was required

    OTP_REQUIRED - otp token was rejected. API consumer may call this endpoint again with correct OTP token.

    AUTH_ERR - invalid OTP token submitted too many times."""
        ...
    def login_with_api_key(self,
        api_key:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Authenticate session using API Key."""
        ...
    def login_with_token(self,
        token:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Authenticate session using token generated with `auth.generate_token`."""
        ...
    def logout(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Deauthenticates an app and if a token exists, removes that from the session."""
        ...
    def me(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> MeReturn:
        """Returns currently logged-in user."""
        ...
    def mechanism_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[str]:
        """Get list of available authentication mechanisms available for auth.login_ex"""
        ...
    def sessions(self,
        filters:_jsonschema.JsonArray=[],
        options:SessionsOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[SessionsAuthSessionQueryResultItem]|SessionsAuthSessionQueryResultItem|int:
        """Returns list of active auth sessions.

Example of return value:

[ {
        "id": "NyhB1J5vjPjIV82yZ6caU12HLA1boDJcZNWuVQM4hQWuiyUWMGZTz2ElDp7Yk87d", "origin": "192.168.0.3:40392", "credentials": "LOGIN_PASSWORD", "credentials_data": {"username": "root"}, "current": True, "internal": False, "created_at": {"$date": 1545842426070} }
]

`credentials` can be `UNIX_SOCKET`, `ROOT_TCP_SOCKET`, `LOGIN_PASSWORD`, `API_KEY` or `TOKEN`, depending on what authentication method was used. For `UNIX_SOCKET` and `LOGIN_PASSWORD` logged-in `username` field will be provided in `credentials_data`. For `API_KEY` corresponding `api_key` will be provided in `credentials_data`. For `TOKEN` its `parent` credential will be provided in `credentials_data`.

If you want to exclude all internal connections from the list, call this method with following arguments:

[ [
        ["internal", "=", True] ]
]"""
        ...
    def set_attribute(self,
        key:str,
        value:_jsonschema.JsonValue,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Set current user's `attributes` dictionary `key` to `value`.

e.g. Setting key="foo" value="var" will result in {"attributes": {"foo": "bar"}}"""
        ...
    def terminate_other_sessions(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Terminates all other sessions (except the current one)."""
        ...
    def terminate_session(self,
        id:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Terminates session `id`."""
        ...
GenerateOnetimePasswordGenerateSingleUsePassword = _ty.TypedDict('GenerateOnetimePasswordGenerateSingleUsePassword', {
    'username': str, 
})
LoginExAuthApiKeyPlain = _ty.TypedDict('LoginExAuthApiKeyPlain', {
    'mechanism': str,
    'username': str,
    'api_key': str,
    'login_options': _ty.NotRequired[_jsonschema.JsonValue], 
})
LoginExAuthPasswordPlain = _ty.TypedDict('LoginExAuthPasswordPlain', {
    'mechanism': str,
    'username': str,
    'password': str,
    'login_options': _ty.NotRequired[_jsonschema.JsonValue], 
})
LoginExAuthTokenPlain = _ty.TypedDict('LoginExAuthTokenPlain', {
    'mechanism': str,
    'token': str,
    'login_options': _ty.NotRequired[_jsonschema.JsonValue], 
})
LoginExAuthOTPToken = _ty.TypedDict('LoginExAuthOTPToken', {
    'mechanism': str,
    'otp_token': str,
    'login_options': _ty.NotRequired[_jsonschema.JsonValue], 
})
LoginExAuthRespSuccess = _ty.TypedDict('LoginExAuthRespSuccess', {
    'response_type': str,
    'user_info': _jsonschema.JsonValue|None,
    'authenticator': str, 
})
LoginExAuthRespAuthErr = _ty.TypedDict('LoginExAuthRespAuthErr', {
    'response_type': str, 
})
LoginExAuthRespExpired = _ty.TypedDict('LoginExAuthRespExpired', {
    'response_type': str, 
})
LoginExAuthRespOTPRequired = _ty.TypedDict('LoginExAuthRespOTPRequired', {
    'response_type': str,
    'username': str, 
})
LoginExAuthRespAuthRedirect = _ty.TypedDict('LoginExAuthRespAuthRedirect', {
    'response_type': str,
    'urls': list[str], 
})
LoginExContinueLoginData = _ty.TypedDict('LoginExContinueLoginData', {
    'mechanism': str,
    'otp_token': str,
    'login_options': _ty.NotRequired[_jsonschema.JsonValue], 
})
LoginExContinueAuthRespSuccess = _ty.TypedDict('LoginExContinueAuthRespSuccess', {
    'response_type': str,
    'user_info': _jsonschema.JsonValue|None,
    'authenticator': str, 
})
LoginExContinueAuthRespAuthErr = _ty.TypedDict('LoginExContinueAuthRespAuthErr', {
    'response_type': str, 
})
LoginExContinueAuthRespExpired = _ty.TypedDict('LoginExContinueAuthRespExpired', {
    'response_type': str, 
})
LoginExContinueAuthRespOTPRequired = _ty.TypedDict('LoginExContinueAuthRespOTPRequired', {
    'response_type': str,
    'username': str, 
})
LoginExContinueAuthRespAuthRedirect = _ty.TypedDict('LoginExContinueAuthRespAuthRedirect', {
    'response_type': str,
    'urls': list[str], 
})
MeReturn = _ty.TypedDict('MeReturn', {
    'pw_name': str,
    'pw_gecos': str,
    'pw_dir': str,
    'pw_shell': str,
    'pw_uid': int,
    'pw_gid': int,
    'grouplist': list[int]|None,
    'sid': str|None,
    'source': str,
    'local': bool,
    'attributes': _jsonschema.JsonObject,
    'two_factor_config': _jsonschema.JsonObject,
    'privilege': _jsonschema.JsonObject,
    'account_attributes': list[str], 
})
SessionsOptions = _ty.TypedDict('SessionsOptions', {
    'relationships': _ty.NotRequired[bool],
    'extend': _ty.NotRequired[str|None],
    'extend_context': _ty.NotRequired[str|None],
    'prefix': _ty.NotRequired[str|None],
    'extra': _ty.NotRequired[_jsonschema.JsonObject],
    'order_by': _ty.NotRequired[list[str]],
    'select': _ty.NotRequired[list[str|_jsonschema.JsonArray]],
    'count': _ty.NotRequired[bool],
    'get': _ty.NotRequired[bool],
    'offset': _ty.NotRequired[int],
    'limit': _ty.NotRequired[int],
    'force_sql_filters': _ty.NotRequired[bool], 
})
SessionsAuthSessionQueryResultItem = _ty.TypedDict('SessionsAuthSessionQueryResultItem', {
    'id': _ty.NotRequired[str],
    'current': _ty.NotRequired[bool],
    'internal': _ty.NotRequired[bool],
    'origin': _ty.NotRequired[str],
    'credentials': _ty.NotRequired[str],
    'credentials_data': _ty.NotRequired[_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue],
    'created_at': _ty.NotRequired[str],
    'secure_transport': _ty.NotRequired[bool], 
})