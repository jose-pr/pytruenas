import typing as _ty
from enum import Enum as _Enum
import re as _re

from . import _utils, _conn, _core
from . import auth as _auth, api as _api


class Namespace:
    _client: "TrueNASClient"

    def __init__(self, client: "TrueNASClient", name: str = None) -> None:
        self._client = client
        self.__namespace = name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._client._target or 'localhost'}/{self._namespace})"

    def __str__(self) -> str:
        return self._namespace

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


class TrueNASClient:
    def __init__(
        self,
        target: str = None,
        creds: "tuple[str,str]|str|dict" = None,
        autologin=True,
        sslverify=True,
    ) -> None:
        self._target = target
        self._creds = _auth.Credentials(creds)
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

    def api(self) -> _api.Api:
        core = Namespace(self, "core")
        services: dict[str, _core.NamespaceInfo] = core.get_services()
        namespaces = []
        for name, service in services.items():
            methods = []
            for name, m in core.get_methods(name).items():
                method = _core.Method._normalize(m)
                name = name.removeprefix(service["config"]["namespace"] + ".")
                descr = method["description"]
                returns = []
                args = _ty.OrderedDict()
                for p in method["accepts"]:
                    pname = p["_name_"].replace("-", "_")
                    args[pname] = _api.Paramater.from_param(p)
                for p in method["returns"]:
                    returns.append(_api.Paramater.from_param(p))
                methods.append(
                    _api.MethodSignature(
                        name=name,
                        description=descr,
                        arguments=args,
                        returns=returns,
                        _src=method,
                    )
                )

            namespaces.append(
                _api.NamespaceSignature(
                    name=service["config"]["namespace"],
                    type=service["type"],
                    description=service["config"]["cli_description"] or '',
                    methods=methods,
                    _src=service,
                )
            )

        return _api.Api("", sorted(namespaces, key=lambda ns: ns.name))

    def _events(self) -> _utils._Dict[_core.Event]:
        core = Namespace(self, "core")
        services: dict[str, _core.Event] = core.get_events()
        return services
