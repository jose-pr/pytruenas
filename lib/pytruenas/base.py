import typing as _ty
from enum import Enum as _Enum
import re as _re

from . import _utils, _conn, _core


class Namespace:
    _client: "TrueNASClient"

    def __init__(self, client: "TrueNASClient", name: str = None) -> None:
        self._client = client
        self.__namespace = name

    @property
    def _namespace(self):
        if not getattr(self, f"_{Namespace.__name__}__namespace", None):
            self.__namespace = _re.sub(
                "[A-Z]+", lambda m: "." + m.group(0).lower(), self.__class__.__name__
            ).strip(".")
        return self.__namespace

    def __call__(self, method: str, *args, **kwds):
        return self._client.call(self._namespace + "." + method, *args, **kwds)

    def __getattr__(self, name: str):
        if isinstance(name, str) and not name.startswith("_"):

            def method(*args, **kwds):
                return self(name, *args, **kwds)

            return method
        else:
            super().__getattribute__(name)


NS = _ty.TypeVar("NS", bound=Namespace)


class AuthMethod(_Enum):
    ApiKey = "login_with_api_key"
    BasicAuth = "login"
    Token = "login_with_token"
    Local = None

    @property
    def auth(self):
        if self != AuthMethod.Local:
            return f"auth.{self.value}"


class Creds(_ty.NamedTuple):
    method: AuthMethod
    args: "_ty.Sequence[str]"

    #
    # Parse a key either from:
    #   (username,password)
    #   (username,password,otp_token)
    #   api_key|token
    #   Mapping with values set by their name
    #
    @classmethod
    def parse(cls, creds: "tuple[str,str]|tuple[str,str,str]|str|dict"):
        if creds:
            ty = None
            if isinstance(creds, Creds):
                ty, args = creds
            elif isinstance(creds, _ty.Mapping):
                key = creds.get("api_key")
                usr = creds.get("username")
                pwd = creds.get("password")
                otp = creds.get("otp_token")
                token = creds.get("token")
                if key:
                    ty = AuthMethod.ApiKey
                    args = [key]
                elif usr and pwd is not None:
                    ty = AuthMethod.BasicAuth
                    args = [usr, pwd, otp]
                elif token:
                    ty = AuthMethod.Token
                    args[token]
                else:
                    raise ValueError("Credentials not supported", creds)
            elif isinstance(creds, (str, bytes)):
                key = _utils.str_(creds)
                #
                # From what i can see an apikey format is <id>-<64 alpha/numeric chars>
                #
                ty = AuthMethod.Token
                try:
                    i, k = key.split("-", maxsplit=1)
                    if i.isnumeric() and k.isalnum() and len(k) == 64:
                        ty = AuthMethod.ApiKey
                except:
                    pass
                args = [key]
            elif isinstance(creds, _ty.Sequence):
                ty = AuthMethod.BasicAuth
                _len = len(creds)
                if _len not in [2, 3]:
                    raise ValueError(
                        "Expected a sequence of (user,password) or (user,password,otp_token)",
                        creds,
                    )
                usr, pwd, otp, *_ = (*creds, None, None)
                args = [usr, pwd, otp]
            if args and args[-1] is None:
                args.pop()
            if not args and ty is not AuthMethod.Local:
                raise ValueError("Only Local authentication doesnt require credentials")
            return Creds(ty, [_utils.str_(arg) for arg in args])
        else:
            return Creds(AuthMethod.Local, [])

    def login(self, client: "TrueNASClient"):
        method = self.method.auth
        if method:
            return client.call(method, *self.args)
        return None


class TrueNASClient:
    def __init__(
        self,
        target: str = None,
        creds: "tuple[str,str]|str|dict" = None,
        autologin=True,
        sslverify=True,
    ) -> None:
        self._target = target
        self._creds = Creds.parse(creds)
        self._conn: _conn.Client = None
        self.sslverify = sslverify
        self.autologin = autologin

    @property
    def uri(self):
        if not self._target or self._target.lower() in ["localhost", "127.0.0.1"]:
            return None
        else:
            return f"wss://{self._target}/websocket"

    @property
    def conn(self):
        if self._conn is None or self._conn._closed.is_set():
            self._conn = _conn.Client(self.uri, sslverify=self.sslverify)
            if self.autologin:
                self._creds.login(self)
        return self._conn

    def call(self, method: str, *args, **kwds):
        return self.conn.call(method, *args, **kwds)

    @_ty.overload
    def namespace(self, name: str) -> Namespace:
        pass

    def namespace(self, name: str, cls: type[NS] = None) -> NS:
        if cls is None:
            cls = Namespace
        return cls(self, name)

    def namespaces(self) -> list[_core.NamespaceInfo]:
        core = Namespace(self, "core")
        services: dict[str, _core.NamespaceInfo] = core.get_services()
        for name, service in services.items():
            service["methods"] = {
                n.removeprefix(
                    service["config"]["namespace"] + "."
                ): _core.Method._normalize(m)
                for n, m in core.get_methods(name).items()
            }
        return list(services.values())

    def _events(self) -> _utils._Dict[_core.Event]:
        core = Namespace(self, "core")
        services: dict[str, _core.NamespaceInfo] = core.get_services()
        return services
