from typing import (
    TypeVar as _TypeVar,
    NamedTuple as _NT,
    Sequence as _Sequence,
    Mapping as _Map,
    Generic as _Generic,
    overload as _overload,
)
import typing as _ty
from enum import Enum as _Enum
import re as _re

from . import _utils, _conn

from typing import TYPE_CHECKING as _TYPING


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


NS = _TypeVar("NS", bound=Namespace)
K = _TypeVar("K", bound=str)
V = _TypeVar("V", bound=str)
T = _TypeVar("T")
D = _TypeVar("D", bound=_ty.TypedDict)
_DStr = dict[str]


class UpdateReturn(_Enum):
    NewValue = 0
    Diff = 1
    Both = 2


class Config(Namespace, _Generic[D]):
    def config(self, normalize: bool = True) -> D:
        config = self("config")
        if normalize:
            f = getattr(D, "_nomalize", None)
            if f:
                config = f(config)
        return config

    @_overload
    def update(
        self,
        __partial: _DStr = None,
        /,
        _return: _ty.Literal[UpdateReturn.NewValue] = UpdateReturn.NewValue,
        _force: bool = False,
        **__named: D,
    ) -> "D":
        ...

    @_overload
    def update(
        self,
        __partial: _DStr = None,
        /,
        _return: _ty.Literal[UpdateReturn.Diff] = UpdateReturn.Diff,
        _force: bool = False,
        **__named: D,
    ) -> "_DStr":
        ...

    @_overload
    def update(
        self,
        __partial: _DStr = None,
        /,
        _return: _ty.Literal[UpdateReturn.Both] = UpdateReturn.Both,
        _force: bool = False,
        **__named: D,
    ) -> "tuple[_DStr,D]":
        ...

    def update(
        self,
        __partial: _DStr = None,
        /,
        _return: UpdateReturn = UpdateReturn.NewValue,
        _force: bool = False,
        **__named: D,
    ) -> "tuple[_DStr,D]|D|_DStr":
        partial = _utils.merge(__partial, __named)
        config = self.config(normalize=True)
        diff = config if _force else _utils.diff(config, partial)
        if diff:
            config = self("update", diff)
        if _return == UpdateReturn.Diff:
            return diff
        elif _return == UpdateReturn.Both:
            return diff, config
        else:
            return config


class Map(Namespace, _Generic[D]):
    _idattr = "id"

    def query(self) -> list[D]:
        return self("query")

    def _as_dict(self, __key=None) -> "_DStr[D]":
        key = __key or self._idattr
        return {item[key]: item for item in self.query()}

    def _parseid(self, id: str | D):
        if isinstance(id, _Map):
            id = id[self._idattr]
        return id

    def get_instance(self, id: str | D):
        id = self._parseid(id)
        return self("get_instance", id)

    def __getitem__(self, __key: str) -> D:
        return self.get_instance(__key)

    def __iter__(self) -> _ty.Iterator[str]:
        return self._as_dict().__iter__()

    def __len__(self) -> int:
        return self("query", [], {"count": True})

    @_overload
    def update(
        self,
        id: str | D,
        __partial: _DStr = None,
        /,
        _return: _ty.Literal[UpdateReturn.NewValue] = UpdateReturn.NewValue,
        _force: bool = False,
        **__named: D,
    ) -> "D":
        ...

    @_overload
    def update(
        self,
        id: str | D,
        __partial: _DStr = None,
        /,
        _return: _ty.Literal[UpdateReturn.Diff] = UpdateReturn.Diff,
        _force: bool = False,
        **__named: D,
    ) -> "_DStr":
        ...

    @_overload
    def update(
        self,
        id: str | D,
        __partial: _DStr = None,
        /,
        _return: _ty.Literal[UpdateReturn.Both] = UpdateReturn.Both,
        _force: bool = False,
        **__named: D,
    ) -> "tuple[_DStr,D]":
        ...

    def update(
        self,
        id: str | D,
        __partial: _DStr = None,
        /,
        _return: UpdateReturn = UpdateReturn.NewValue,
        _force: bool = False,
        **__named: D,
    ) -> "tuple[_DStr,D]|D|_DStr":
        partial = _utils.merge(__partial, __named)
        if isinstance(id, _Map):
            config = id
        else:
            config = self.get_instance(id)
        id = self._parseid(id)
        diff = config if _force else _utils.diff(config, partial)
        if diff:
            config = self("update", id, diff)
        if _return == UpdateReturn.Diff:
            return diff
        elif _return == UpdateReturn.Both:
            return diff, config
        else:
            return config


class MapExtended(Map[D], _Map[str, D], _Generic[D]):
    ...


class AuthMethod(_Enum):
    ApiKey = "login_with_api_key"
    BasicAuth = "login"
    Token = "login_with_token"
    Local = None

    @property
    def auth(self):
        if self != AuthMethod.Local:
            return f"auth.{self.value}"


class Creds(_NT):
    method: AuthMethod
    args: "_Sequence[str]"

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
            elif isinstance(creds, _Map):
                key = creds.get("api_key")
                usr = creds.get("username")
                pwd = creds.get("password")
                otp = creds.get("otp_token")
                token = creds.get('token')
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
                    i, k = key.split('-', maxsplit=1) 
                    if i.isnumeric() and k.isalnum() and len(k) == 64:
                        ty = AuthMethod.ApiKey
                except:
                    pass
                args = [key]
            elif isinstance(creds, _Sequence):
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

    @_overload
    def namespace(self, name: str) -> Namespace:
        pass

    def namespace(self, name: str, cls: type[NS] = None) -> NS:
        if cls is None:
            cls = Namespace
        return cls(self, name)
