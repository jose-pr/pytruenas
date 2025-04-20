import errno
import time

from . import _conn
from . import auth as _auth

import logging


class Namespace:
    _client: "TrueNASClient"

    def __init__(self, client: "TrueNASClient", *name: str) -> None:
        self._client = client
        self._namespace = ".".join([n for n in name if n])

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._client._target}/{self._namespace.replace('.','/')})"

    def __str__(self) -> str:
        return self._namespace

    def __call__(self, *args, _tries=1, _method: str = None, **kwds):
        method = self._namespace
        if _method:
            method = f"{method}.{_method}"
        while _tries > 0:
            try:
                self._client.logger.trace(f"Calling method: {method}")
                return self._client.conn.call(method, *args, **kwds)
            except _conn.ClientException as e:
                if e.errno == errno.ECONNABORTED and _tries:
                    _tries -= 1
                    self._conn = None
                    time.sleep(1)
                else:
                    raise e

    def __getattr__(self, name: str):
        if isinstance(name, str) and not name.startswith("_"):
            return Namespace(self._client, self._namespace, name.removesuffix('_'))
        else:
            super().__getattribute__(name)


class TrueNASClient:
    def __init__(
        self,
        target: str = None,
        creds: "tuple[str,str]|str|dict" = None,
        autologin=True,
        sslverify=True,
        *,
        api=None,
        logger: logging.Logger = None,
    ) -> None:
        self._target = target or "localhost"
        self._creds = _auth.Credentials(creds)
        self._conn: _conn.JSONRPCClient = None
        self.sslverify = sslverify
        self.autologin = autologin
        self.api_uri = api or self._target
        if not logger:
            logger = logging.getLogger("pytruenas")
        self.logger = logging.getLogger(logger) if isinstance(logger, str) else logger

    @property
    def api_uri(self):
        return self._api

    @api_uri.setter
    def api_uri(self, value: str):
        if not value or value.lower() in ["localhost", "127.0.0.1"]:
            self._api = None
        else:
            self._api = f"wss://{value}/api/current"

    @property
    def conn(self):
        if self._conn is None or self._conn._closed.is_set():
            self._conn = _conn.Client(self.api_uri, verify_ssl=self.sslverify)
            if self.autologin:
                self._creds.login(self)
        return self._conn

    @property
    def api(self):
        return Namespace(self)
