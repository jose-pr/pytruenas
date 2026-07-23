from __future__ import annotations

import typing as _ty
from .utils import io as _ioutils
if _ty.TYPE_CHECKING:
    from . import TrueNASClient


class _CredentialsMeta(type):
    def __call__(
        cls: "type[Credentials]",  # type:ignore
        *args,
        **kwargs
    ):
        if cls is not Credentials:
            inst = cls.__new__(cls, *args, **kwargs)
            inst.__init__(*args, **kwargs)
            return inst
        if not (args or kwargs):
            return LocalAuth()
        if args and kwargs:
            raise AttributeError(args, kwargs)
        if args and len(args) == 1:
            cred = args[0]
            if cred is None:
                return LocalAuth()
            if isinstance(cred, Credentials):
                return cred
            if isinstance(cred, (list, tuple)):
                return BasicAuth(*cred)
            cred = _ioutils.str_(cred)
            if ":" in cred:
                # : is not valid char in key or token assume is user/pass
                usr, pwd = cred.split(":", maxsplit=1)
                if "\n" in pwd:
                    # assume newline not a common/valid password char
                    pwd, token = pwd.split("\n", maxsplit=1)
                else:
                    token = None
                return BasicAuth(usr, pwd, token)
            else:
                #
                # An api key looks like <id>-<64 alphanumeric chars>; anything
                # else that is a bare string (no ':') is treated as a token.
                #
                try:
                    i, k = cred.split("-", maxsplit=1)
                    is_api_key = i.isnumeric() and k.isalnum() and len(k) == 64
                except ValueError:
                    # No "-" to unpack -> not an api key. A ValueError is the
                    # only thing split/unpack raises here; anything else is a
                    # real bug and should surface, not be swallowed.
                    is_api_key = False
                return ApiKeyAuth(cred) if is_api_key else TokenAuth(cred)
        elif args:
            return BasicAuth(*args)
        else:
            for scls in Credentials.__subclasses__():
                try:
                    return scls(**kwargs)
                except TypeError:
                    # These kwargs don't fit this subclass's __init__ -> try the
                    # next. Narrowed from `except Exception` so a genuine bug in
                    # a subclass __init__ surfaces instead of being hidden behind
                    # the generic "Credentials not supported" below.
                    pass

        # Mask secret-bearing values: this exception (with its args) is likely
        # to be logged, and the raw kwargs carry the password/token/api_key.
        _secret = {"password", "passwd", "token", "api_key", "apikey", "secret"}
        safe_kwargs = {
            k: ("***" if k.lower() in _secret and v else v) for k, v in kwargs.items()
        }
        raise ValueError("Credentials not supported", safe_kwargs)


class AuthenticationError(Exception):
    """A modern ``auth.login_ex`` login was refused.

    ``response_type`` is the server's discriminator (``AUTH_ERR``/``DENIED``/
    ``EXPIRED``/…); ``response`` is the full response dict for callers that need
    the detail (e.g. a ``REDIRECT`` target).
    """

    def __init__(self, response_type: str, response: dict) -> None:
        super().__init__(f"login_ex failed: {response_type}")
        self.response_type = response_type
        self.response = response


class Credentials(metaclass=_CredentialsMeta):
    #: Legacy ``auth.*`` method name (``login``/``login_with_api_key``/
    #: ``login_with_token``) for the classic :meth:`login` path.
    METHOD = None
    #: Modern ``auth.login_ex`` mechanism name (``PASSWORD_PLAIN``/
    #: ``API_KEY_PLAIN``/``TOKEN_PLAIN``). ``None`` means this credential has no
    #: login_ex form (e.g. local-socket auth) -- :meth:`login_ex` falls back.
    MECHANISM: "str | None" = None

    def __init__(self, *args, **kwargs) -> None:
        pass

    def _args(self) -> _ty.Iterable:
        raise NotImplementedError()

    def login(self, client: "TrueNASClient"):
        """Legacy login via ``auth.login``/``login_with_*`` (unchanged)."""
        if self.METHOD:
            return client.api.auth[self.METHOD](*self._args())
        return None

    # -- modern login_ex path ----------------------------------------------

    def _login_data(self) -> "dict | None":
        """The ``login_ex`` payload for this credential, or ``None`` if it has
        no login_ex mechanism (falls back to legacy :meth:`login`)."""
        return None

    def login_ex(
        self,
        client: "TrueNASClient",
        *,
        login_options: "dict | None" = None,
        otp_provider: "_ty.Callable[[], str] | None" = None,
    ) -> "dict | None":
        """Authenticate via the modern ``auth.login_ex`` mechanism.

        Handles the discriminated response: ``SUCCESS`` returns the response
        dict; ``OTP_REQUIRED`` calls ``auth.login_ex_continue`` with an OTP
        token (from this credential's own ``otp_token`` if set, else from
        ``otp_provider()`` if given, else raises); any other ``response_type``
        raises :class:`AuthenticationError`. A credential with no login_ex
        mechanism (e.g. :class:`LocalAuth`) falls back to legacy :meth:`login`.

        ``login_options`` overrides the server defaults (``{"user_info": True,
        "reconnect_token": False}``).
        """
        data = self._login_data()
        if data is None:  # no login_ex form -> legacy path
            self.login(client)
            return None
        if login_options is not None:
            data = {**data, "login_options": login_options}

        resp = client.api.auth.login_ex(data)
        resp = _ty.cast(dict, resp) or {}
        rtype = resp.get("response_type")

        if rtype == "OTP_REQUIRED":
            otp = getattr(self, "otp_token", None)
            if not otp and otp_provider is not None:
                otp = otp_provider()
            if not otp:
                raise AuthenticationError("OTP_REQUIRED", resp)
            resp = _ty.cast(
                dict,
                client.api.auth.login_ex_continue(
                    {"mechanism": "OTP_TOKEN", "otp_token": otp}
                ),
            ) or {}
            rtype = resp.get("response_type")

        if rtype == "SUCCESS":
            return resp
        raise AuthenticationError(rtype or "UNKNOWN", resp)

    @staticmethod
    def from_env(env: _ty.Mapping | None = None):
        if env is None:
            import os

            env = os.environ
        return Credentials(env.get("TN_CREDS"))


class LocalAuth(Credentials):
    def _args(self):
        return []


class ApiKeyAuth(Credentials):
    METHOD = "login_with_api_key"
    MECHANISM = "API_KEY_PLAIN"

    def __init__(self, api_key: str, username: str | None = None) -> None:
        self.api_key = api_key
        # login_ex's API_KEY_PLAIN wants the username too; the legacy
        # login_with_api_key does not. If unknown, the modern path can't be used
        # and login_ex falls back to legacy.
        self.username = username

    def _args(self):
        return [self.api_key]

    def _login_data(self):
        if not self.username:
            return None  # no username -> use legacy login_with_api_key
        return {
            "mechanism": "API_KEY_PLAIN",
            "username": self.username,
            "api_key": self.api_key,
        }


class TokenAuth(Credentials):
    METHOD = "login_with_token"
    MECHANISM = "TOKEN_PLAIN"

    def __init__(self, token: str) -> None:
        self.token = token

    def _args(self):
        return [self.token]

    def _login_data(self):
        return {"mechanism": "TOKEN_PLAIN", "token": self.token}


class BasicAuth(Credentials):
    METHOD = "login"
    MECHANISM = "PASSWORD_PLAIN"

    def __init__(
        self, username: str, password: str, otp_token: str | None = None
    ) -> None:
        self.username = username
        self.password = password
        self.otp_token = otp_token

    def _args(self):
        args = [self.username, self.password]
        if self.otp_token:
            args.append(self.otp_token)
        return args

    def _login_data(self):
        return {
            "mechanism": "PASSWORD_PLAIN",
            "username": self.username,
            "password": self.password,
        }