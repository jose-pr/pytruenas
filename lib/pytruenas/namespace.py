from functools import cache
import typing as _ty
import errno as _errno
import time as _time

import re as _re

from . import _conn, _utils
from .utils import query as _q

if _ty.TYPE_CHECKING:
    from . import TrueNASClient

_ERRNO_PATTERN = _re.compile(r"^\[([^]]*)\]\s*(.*)")


def ioerror(error: _conn.ClientException):
    match = _ERRNO_PATTERN.match(error.error)
    if match:
        name = match[1]
        msg = match[2]

        errno = getattr(_errno, name, None)
        if error is not None:

            error = IOError(errno, msg)

    return error


class Namespace:
    _client: "TrueNASClient"

    def __init__(self, client: "TrueNASClient", *name: str) -> None:
        self._client = client
        self._namespace = ".".join([n for n in name if n])

    @cache
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._client._api}/{self._namespace.replace('.','/')})"

    def __str__(self) -> str:
        return self._namespace

    def __call__(
        self,
        *args,
        _tries=1,
        _method: str = None,
        _ioerror=False,
        _filetransfer: bool | bytes = False,
        **kwds,
    ):
        method = self._namespace
        if _method:
            method = f"{method}.{_method}"
        if _filetransfer is True:
            return self._client.download(
                method,
                *args,
                _ioerror=_ioerror,
                **kwds,
            )
        elif _utils.isbytelike(_filetransfer) or hasattr(_filetransfer, 'read'):
            return self._client.upload(
                _filetransfer,
                method,
                *args,
                _ioerror=_ioerror,
                **kwds,
            )
        elif _filetransfer:
            raise TypeError(_filetransfer)
        
        while _tries > 0:
            try:
                self._client.logger.trace(f"Calling method: {method} args: {args}")
                return self._client.websocket.call(method, *args, **kwds)
            except _conn.ClientException as e:
                if e.errno == _errno.ECONNABORTED and _tries:
                    self._client.logger.warning(
                        f"Websocket connection was closed, trying again with new connection"
                    )
                    _tries -= 1
                    self._conn = None
                    _time.sleep(1)
                else:
                    raise ioerror(e) if _ioerror else e from None

    if not _ty.TYPE_CHECKING:
        @cache
        def __getattr__(self, name: str) -> "Namespace":
            if isinstance(name, str) and not name.startswith("_"):
                return self[name.removesuffix("_")]
            else:
                super().__getattribute__(name)

    else:

        def __getattr__(self, name: str) -> "Namespace": ...

    @cache
    def __getitem__(self, name:str) -> "Namespace":
         return Namespace(self._client, self._namespace, name)

    def _query(self, *__opts: dict | _q.Option, **filter) -> list[dict[str]]:
        opts = _q.Option.options(*__opts)
        filter = _q.filter_from_kwargs(**filter)
        return self.query(filter, opts)

    def _get(self, __id = None, **filter) -> dict[str]:
        if __id is not None and filter:
            raise ValueError(filter)
        
        if __id is not None:
            try:
                return self.get_instance(__id, _ioerror=True)
            except FileNotFoundError as e:
                return None
        
        result = self._query({"limit": 1}, **filter)
        if result:
            return result[0]

    def _upsert(
        self, __unique: str | _ty.Sequence[str], *__opts: dict | _q.Option, **fields
    ) -> dict[str]:
        opts = _q.Option.options(*__opts)
        idkey = opts.get("idkey") or "id"
        unique = __unique or idkey
        fields = {name: val for name, val in fields.items() if val is not _q.EXCLUDE}
        if isinstance(unique, str):
            unique = (unique,)
        current = self._get(**{name: fields[name] for name in unique})
        if current:
            exclude = (idkey, unique, *(opts.get("update_exclude") or []))
            fields = {name: val for name, val in fields.items() if name not in exclude}
            result = self.update(current[idkey], fields)
        else:
            exclude = (idkey, *(opts.get("create_exclude") or []))
            fields = {name: val for name, val in fields.items() if name not in exclude}
            result = self.create(fields)

        wait = opts.get("wait", True)
        if isinstance(result, int) and (wait is None or wait):
            result = self._client.api.core.job_wait(result, job=True)

        return result
