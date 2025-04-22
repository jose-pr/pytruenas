from pytruenas import Namespace as _NS 
class Auth(_NS):
    
    def generate_onetime_password(self,
        generate_single_use_password,
    ) -> AuthGenerate_onetime_password:
        """Generate a password for the specified username that may be used only a single time to authenticate to TrueNAS. This may be used by server administrators to allow users authenticate and then set a proper password and two-factor authentication token."""
        ...
    def generate_token(self,
        ttl,
        attrs,
        match_origin,
        single_use,
    ) -> AuthGenerate_token:
        """Generate a token to be used for authentication.

`ttl` stands for Time To Live, in seconds. The token will be invalidated if the connection has been inactive for a time greater than this.

`attrs` is a general purpose object/dictionary to hold information about the token.

`match_origin` will only allow using this token from the same IP address or with the same user UID.

NOTE: this endpoint is not supported when server security requires replay-resistant authentication as part of GPOS STIG requirements."""
        ...
    def login(self,
        username,
        password,
        otp_token,
    ) -> AuthLogin:
        """Authenticate session using username and password. `otp_token` must be specified if two factor authentication is enabled."""
        ...
    def login_ex(self,
        login_data,
    ) -> AuthLogin_ex:
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
        login_data,
    ) -> AuthLogin_ex_continue:
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
        api_key,
    ) -> AuthLogin_with_api_key:
        """Authenticate session using API Key."""
        ...
    def login_with_token(self,
        token,
    ) -> AuthLogin_with_token:
        """Authenticate session using token generated with `auth.generate_token`."""
        ...
    def logout(self,
    ) -> AuthLogout:
        """Deauthenticates an app and if a token exists, removes that from the session."""
        ...
    def me(self,
    ) -> AuthMe:
        """Returns currently logged-in user."""
        ...
    def mechanism_choices(self,
    ) -> AuthMechanism_choices:
        """Get list of available authentication mechanisms available for auth.login_ex"""
        ...
    def sessions(self,
        filters,
        options,
    ) -> AuthSessions:
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
        key,
        value,
    ) -> AuthSet_attribute:
        """Set current user's `attributes` dictionary `key` to `value`.

e.g. Setting key="foo" value="var" will result in {"attributes": {"foo": "bar"}}"""
        ...
    def terminate_other_sessions(self,
    ) -> AuthTerminate_other_sessions:
        """Terminates all other sessions (except the current one)."""
        ...
    def terminate_session(self,
        id,
    ) -> AuthTerminate_session:
        """Terminates session `id`."""
        ...
class AuthGenerate_onetime_password:
    ...
class AuthGenerate_token:
    ...
class AuthLogin:
    ...
class AuthLogin_ex:
    ...
class AuthLogin_ex_continue:
    ...
class AuthLogin_with_api_key:
    ...
class AuthLogin_with_token:
    ...
class AuthLogout:
    ...
class AuthMe:
    ...
class AuthMechanism_choices:
    ...
class AuthSessions:
    ...
class AuthSet_attribute:
    ...
class AuthTerminate_other_sessions:
    ...
class AuthTerminate_session:
    ... 