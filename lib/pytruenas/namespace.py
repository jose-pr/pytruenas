from functools import cache
import typing as _ty
import errno as _errno
import time as _time

import re as _re
import enum as _enum

from . import _conn
from .utils import query as _q, io as _ioutils

if _ty.TYPE_CHECKING:
    from . import TrueNASClient

_ERRNO_PATTERN = _re.compile(r"^\[([^]]*)\]\s*(.*)")


def ioerror(error: _conn.ClientException) -> Exception:
    match = _ERRNO_PATTERN.match(error.error)
    if match:
        name = match[1]
        msg = match[2]

        errno = getattr(_errno, name, None)
        if error is not None:

            return IOError(errno, msg)

    return error


_T = _ty.TypeVar("_T", bound=dict[str, object])

_DBSelector: _ty.TypeAlias = "int | str | _ty.Sequence[str] | None | _q._Exclude"


class DbAction(_ty.Generic[_T], _enum.StrEnum):
    CREATE = "create"
    UPDATE = "update"
    UPSERT = "upsert"

    def execute(
        __action,
        __namespace: "Namespace",
        __selector: _DBSelector = None,
        *__opts: dict | _q.Option | tuple[str,object],
        **__fields,
    ) -> _T:
        opts = _q.Option.options(*__opts)
        idkey = opts.get("idkey") or "id"
        callback = opts.get("callback") or None
        fields = {name: val for name, val in __fields.items() if val is not _q.EXCLUDE}

        if isinstance(__selector, str) or not isinstance(__selector, _ty.Iterable):
            _id = __selector
            selectors = {}
        else:
            _id = None
            selectors = (
                __selector
                if isinstance(__selector, _ty.Mapping)
                else {
                    selector.removeprefix("!"): (
                        _q.EXCLUDE if selector.startswith("!") else fields[selector]
                    )
                    for selector in __selector
                }
            )

        if _id is None and selectors:
            current = __namespace._get(**selectors)
            if current:
                _id = _ty.cast(int, current[idkey])
        else:
            current = None

        if _id is None and not selectors:
            result = __namespace.update(fields)
            action = DbAction.UPDATE
        elif _id not in (None, _q.EXCLUDE):
            if __action not in (DbAction.UPDATE, DbAction.UPSERT):
                raise FileExistsError(_id)
            exclude = (idkey, *(opts.get("update_exclude") or []))
            fields = {
                name: val
                for name, val in fields.items()
                if name not in exclude and selectors.get(name) not in (val, _q.EXCLUDE)
            }
            if fields:
                result = __namespace.update(_id, fields)
            else:
                result = None

            if result == _id:
                result = __namespace._get(_id)
            elif result is None:
                result = __namespace._get(_id) if not current else current
            action = DbAction.UPDATE
        else:
            if __action not in (DbAction.CREATE, DbAction.UPSERT):
                raise FileNotFoundError(selectors)
            exclude = (idkey, *(opts.get("create_exclude") or []))
            fields = {name: val for name, val in fields.items() if name not in exclude}
            result = __namespace.create(fields)
            action = DbAction.CREATE

        wait = opts.get("wait", True)
        if isinstance(result, int) and (wait is None or wait):
            result = __namespace._client.api.core.job_wait(result, job=True)

        result = _ty.cast(_T, result)

        if callable(callback):
            callback(action, _id, result)

        return result


class Namespace:
    _client: "TrueNASClient"

    def __init__(self, client: "TrueNASClient", *name: str) -> None:
        self._client = client
        self._namespace = ".".join([n for n in name if n])

    @cache
    def __repr__(self) -> str:  # type:ignore
        return f"{self.__class__.__name__}({self._client._api}/{self._namespace.replace('.','/')})"

    def __str__(self) -> str:
        return self._namespace

    def __call__(
        self,
        *args,
        _tries=1,
        _method: str | None = None,
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
        elif _ioutils.isbytelike(_filetransfer) or hasattr(_filetransfer, "read"):
            return self._client.upload(
                _ty.cast(bytes, _filetransfer),
                method,
                *args,
                _ioerror=_ioerror,
                **kwds,
            )
        elif _filetransfer:
            raise TypeError(_filetransfer)

        while _tries > 0:
            try:
                self._client.logger.trace(  # type:ignore
                    f"Calling method: {method} args: {args}"
                )
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
    def __getitem__(self, name: str) -> "Namespace":
        return Namespace(self._client, self._namespace, name)

    def _query(self, *__opts: dict | _q.Option, **filter):
        opts = _q.Option.options(*__opts)
        filter = _q.filter_from_kwargs(**filter)
        return _ty.cast(list[dict[str, object]], self.query(filter, opts))

    def _get(
        self,
        __id_or_filter: _ty.Mapping | int | str | None | _q._Exclude = None,
        **__filter,
    ) -> dict[str, object] | None:
        if isinstance(__id_or_filter, _ty.Mapping):
            id = None
            filter = {**__id_or_filter}
            filter.update(__filter)
        else:
            id = __id_or_filter if __id_or_filter is not _q.EXCLUDE else None
            filter = __filter
        if id is not None and filter:
            raise ValueError(__filter)

        if id is not None:
            try:
                return _ty.cast(dict[str, object], self.get_instance(id, _ioerror=True))
            except FileNotFoundError as e:
                return None

        result = self._query({"limit": 1}, **filter)
        if result:
            return result[0]

    def _upsert(
        self,
        __selector: _DBSelector = None,
        __callback: (
            _ty.Callable[[DbAction, str | int, dict[str, object]], None] | None
        ) = None,
        *__opts: dict | _q.Option,
        **__fields,
    ):
        return DbAction.UPSERT.execute(
            self, __selector, ("callback", __callback), *__opts, **__fields
        )

    def _update(
        self,
        __selector: _DBSelector = None,
        *__opts: dict | _q.Option,
        **__fields,
    ):
        return DbAction.UPDATE.execute(self, __selector, *__opts, **__fields)

    def _create(
        self,
        *__opts: dict | _q.Option,
        **__fields,
    ):
        return DbAction.CREATE.execute(self, _q.EXCLUDE, *__opts, **__fields)
