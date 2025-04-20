import errno
import time
import typing as _ty

from . import _conn
from . import auth as _auth

import logging

from .utils import sql as _sql


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
                self._client.logger.trace(f"Calling method: {method} args: {args}")
                return self._client.conn.call(method, *args, **kwds)
            except _conn.ClientException as e:
                if e.errno == errno.ECONNABORTED and _tries:
                    _tries -= 1
                    self._conn = None
                    time.sleep(1)
                else:
                    raise e

    def __getattr__(self, name: str) -> "Namespace":
        if isinstance(name, str) and not name.startswith("_"):
            return Namespace(self._client, self._namespace, name.removesuffix("_"))
        else:
            super().__getattribute__(name)

    def _query(self, *__opts: dict|_sql.Option, **filter) -> list[dict[str]]:
        opts = _sql.Option.options(*__opts)
        filter = _sql.filter_from_kwargs(**filter)
        return self.query(filter, opts)

    def _get(self, **filter) -> dict[str]:
        result = self._query({"limit": 1}, **filter)
        if result:
            return result[0]

    def _upsert(self, __unique: str | _ty.Sequence[str], *__opts: dict|_sql.Option, **fields) -> dict[str]:
        opts = _sql.Option.options(*__opts)
        idkey = opts.get('idkey') or "id"
        unique = __unique or idkey
        if isinstance(unique, str):
            unique = (unique,)
        current = self._get(**{name: fields[name] for name in unique})
        if current:
            exclude = (idkey, unique, *(opts.get('update_exclude') or []))
            fields = {name: val for name, val in fields.items() if name not in exclude}
            result = self.update(current[idkey], **fields)
        else:
            exclude = (idkey, *(opts.get('create_exclude') or []))
            fields = {name: val for name, val in fields.items() if name not in exclude}
            result = self.create(**fields)
        
        return result


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
