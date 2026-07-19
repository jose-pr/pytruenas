from __future__ import annotations

import typing as _ty
import errno as _errno
import time as _time

import re as _re
import enum as _enum

from . import _conn
from .utils import query as _q, io as _ioutils

if _ty.TYPE_CHECKING:
    from . import TrueNASClient


class _Unset:
    """Sentinel type for "argument not supplied" (distinct from ``None``)."""


#: Marks a ``_timeout`` argument as "use the client default" -- ``None`` is a
#: real value meaning "wait indefinitely", so it cannot double as the default.
_UNSET = _Unset()

_ERRNO_PATTERN = _re.compile(r"^\[([^]]*)\]\s*(.*)")


def ioerror(error: _conn.ClientException) -> Exception:
    """Map a middleware ``[ERRNO] message`` error to the matching ``OSError``.

    Only errors whose bracketed prefix names a real POSIX errno become an
    ``OSError`` (with that ``errno``); anything else is returned unchanged. The
    prior ``if error is not None`` guard was always true, so an unrecognised
    prefix produced ``IOError(None, msg)`` — losing the original exception type.
    """
    match = _ERRNO_PATTERN.match(error.error)
    if match:
        name = match[1]
        msg = match[2]
        errno = getattr(_errno, name, None)
        if errno is not None:
            return IOError(errno, msg)

    return error


_T = _ty.TypeVar("_T", bound="dict[str, object]")

_DBSelector = "int | str | _ty.Sequence[str] | None | _q._Exclude"


class DbAction(str, _enum.Enum):
    """The database mutation an ``_upsert``/``_update``/``_create`` resolves to.

    A ``str`` enum (``StrEnum`` is 3.11+, so this uses the 3.9-compatible
    ``(str, Enum)`` form) whose members double as the action name.
    """

    CREATE = "create"
    UPDATE = "update"
    UPSERT = "upsert"

    def execute(
        __action,
        __namespace: "Namespace",
        __selector: _DBSelector = None,
        *__opts: dict | _q.Option | tuple[str, object],
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

        force: bool = opts.get("force", False)
        action = None
        if _id is None and not selectors:
            if not force:
                result = _ty.cast(dict[str, object], __namespace.config())
                fields = _q.diff(result, fields)
            else:
                result = None
            if fields:
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

            if not force:
                if not current:
                    current = _ty.cast(dict[str, object], __namespace._get(_id))
                fields = _q.diff(current, fields)

            if fields:
                result = __namespace.update(_id, fields)
                action = DbAction.UPDATE
            else:
                result = None

            if result == _id:
                result = __namespace._get(_id)
            elif result is None:
                result = __namespace._get(_id) if not current else current
        else:
            if __action not in (DbAction.CREATE, DbAction.UPSERT):
                raise FileNotFoundError(selectors)
            exclude = (idkey, *(opts.get("create_exclude") or []))
            fields = {name: val for name, val in fields.items() if name not in exclude}
            try:
                result = __namespace.create(fields)
            except _conn.ValidationErrors as e:
                if "already exists" in e.error:
                    raise FileExistsError(e.error)
                else:
                    raise e
            action = DbAction.CREATE

        wait = opts.get("wait", True)
        if isinstance(result, int) and (wait is None or wait):
            result = __namespace._client.api.core.job_wait(result, job=True, _timeout=None)

        result = _ty.cast(_T, result)

        if callable(callback):
            callback(action, _id, result)

        return result


class Namespace:
    _client: "TrueNASClient"

    def __init__(self, client: "TrueNASClient", *name: str) -> None:
        self._client = client
        self._namespace = ".".join([n for n in name if n])
        # Per-instance child cache. Using functools.cache on the methods keyed
        # the cache on ``self``, pinning every Namespace for the process
        # lifetime (uncollectable) -- fine for the CLI, a leak for a long-lived
        # embedding client. A plain dict is dropped with the instance.
        self._children: "dict[str, Namespace]" = {}

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
        _timeout: "float | None | _Unset" = _UNSET,
        **kwds,
    ):
        """Invoke this namespace's middleware method.

        ``_tries`` is the number of *reconnect retries* after a dropped
        connection (``ECONNABORTED``); with the default 1 the call is attempted
        up to twice. ``_timeout`` is the per-call timeout in seconds; the
        default sentinel uses the client's configured timeout, ``None`` waits
        indefinitely (used by ``core.job_wait`` for long jobs). ``_method``
        appends a leaf method name, ``_ioerror`` maps a middleware error to the
        matching ``OSError``, and ``_filetransfer`` routes through
        upload/download.
        """
        method = self._namespace
        if _method:
            method = f"{method}.{_method}"
        # _ioerror is only meaningful for the direct-call path below; the
        # transfer helpers don't accept it (it would leak into their **kwargs
        # and on to generate_token/core.download), so it is intentionally not
        # forwarded here.
        if _filetransfer is True:
            return self._client.download(method, *args, **kwds)
        elif _ioutils.isbytelike(_filetransfer) or hasattr(_filetransfer, "read"):
            return self._client.upload(
                _ty.cast(bytes, _filetransfer), method, *args, **kwds
            )
        elif _filetransfer:
            raise TypeError(_filetransfer)

        if _timeout is not _UNSET:
            kwds["timeout"] = _timeout

        # One initial attempt plus `_tries` reconnect retries after an aborted
        # connection. The loop always ends in a return or a raise -- it must
        # never fall through to None (a None here reads as "no result" and, via
        # _get, silently turns an upsert into a create).
        attempts = max(0, _tries) + 1
        last_exc: "_conn.ClientException | None" = None
        for attempt in range(attempts):
            try:
                self._client.logger.trace(  # type:ignore
                    f"Calling method: {method} args: {args}"
                )
                return self._client.websocket.call(method, *args, **kwds)
            except _conn.ClientException as e:
                last_exc = e
                if e.errno == _errno.ECONNABORTED and attempt < attempts - 1:
                    self._client.logger.warning(
                        "Websocket connection was closed, trying again with new connection"
                    )
                    # Drop the dead connection on the CLIENT so the next
                    # `websocket` access reconnects (setting it on self, a
                    # Namespace, was a no-op that only worked by accident).
                    self._client._conn = None
                    _time.sleep(1)
                    continue
                raise (ioerror(e) if _ioerror else e) from None
        # Unreachable in practice (the loop returns or raises), but guarantees
        # we never return None on a connection error.
        raise ioerror(last_exc) if _ioerror else last_exc  # type: ignore[misc]

    if not _ty.TYPE_CHECKING:

        def __getattr__(self, name: str) -> "Namespace":
            if isinstance(name, str) and not name.startswith("_"):
                return self[name.removesuffix("_")]
            # A private/dunder miss is a real AttributeError, not a namespace --
            # ``__getattribute__`` raises it (the previous code dropped the
            # ``return``/``raise`` and silently returned None).
            return super().__getattribute__(name)

    else:

        def __getattr__(self, name: str) -> "Namespace": ...

    def __getitem__(self, name: str) -> "Namespace":
        child = self._children.get(name)
        if child is None:
            child = self._children[name] = Namespace(self._client, self._namespace, name)
        return child

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
            except FileNotFoundError:
                return None

        result = self._query({"limit": 1}, **filter)
        if result:
            return result[0]

    def _upsert(
        self,
        __selector: _DBSelector = None,
        __callback: (
            _ty.Callable[[DbAction, str | int, dict[str, object]], None]
            | None
            | dict
            | _q.Option
            | _ty.Tuple[str, object]
        ) = None,
        *__opts: dict | _q.Option | _ty.Tuple[str, object],
        **__fields,
    ):
        opts = [*__opts]
        if callable(__callback):
            opts.append(("callback", __callback))
        elif __callback:
            opts.append(__callback)

        return DbAction.UPSERT.execute(self, __selector, *opts, **__fields)

    def _update(
        self,
        __selector: _DBSelector = None,
        *__opts: dict | _q.Option | _ty.Tuple[str, object],
        **__fields,
    ):
        return DbAction.UPDATE.execute(self, __selector, *__opts, **__fields)

    def _create(
        self,
        *__opts: dict | _q.Option | _ty.Tuple[str, object],
        **__fields,
    ):
        return DbAction.CREATE.execute(self, _q.EXCLUDE, *__opts, **__fields)
