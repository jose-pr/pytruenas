from __future__ import annotations

import typing as _ty
import errno as _errno
import time as _time

import re as _re
import enum as _enum

from . import auth as _auth
from . import connection as _connection
from .utils import query as _q, io as _ioutils

#: duho's TRACE level, by number: `log()` works on any logger a caller assigns,
#: including one whose class has no `.trace()`.
_TRACE = 5

if _ty.TYPE_CHECKING:
    from . import TrueNASClient


class _Unset:
    """Sentinel type for "argument not supplied" (distinct from ``None``)."""


#: Marks a ``_timeout`` argument as "use the client default" -- ``None`` is a
#: real value meaning "wait indefinitely", so it cannot double as the default.
_UNSET = _Unset()

_ERRNO_PATTERN = _re.compile(r"^\[([^]]*)\]\s*(.*)", _re.S)
_ERRNO_NUMBER = _re.compile(r"Errno (\d+)")


def ioerror(error: _connection.ClientException) -> Exception:
    """Map a middleware ``[ENAME] message`` error to the matching ``OSError``.

    The bracketed prefix comes in two spellings: a symbolic name
    (``[ENOENT] ...``) and a relayed Python ``OSError`` (``[Errno 2] ...`` --
    what ``filesystem.mkdir`` sends for a missing parent). Both become an
    ``OSError`` with that ``errno``, so the caller gets the builtin subclass
    (``FileNotFoundError``...) that pathlib code branches on; anything else is
    returned unchanged.
    """
    match = _ERRNO_PATTERN.match(error.error)
    if match:
        name = match[1]
        msg = match[2]
        errno = getattr(_errno, name, None)
        if errno is None:
            number = _ERRNO_NUMBER.fullmatch(name)
            errno = int(number[1]) if number else None
        if errno is not None:
            return OSError(errno, msg)

    return error


_T = _ty.TypeVar("_T", bound="dict[str, object]")

_DBSelector = _ty.Optional[_ty.Union[int, str, _ty.Sequence[str], _q._Exclude]]


class DBAction(str, _enum.Enum):
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
        *__opts: _ty.Union[dict, _q.Option, tuple[str, object]],
        **__fields,
    ) -> _T:
        opts = _q.Option.options(*__opts)
        idkey = opts.get("idkey") or "id"
        callback = opts.get("callback") or None
        wait = opts.get("wait", True)
        job = opts.get("job")

        def run(leaf: str, *params):
            # A job answers with its id; whether this method is one comes from
            # the caller (`job`) or the method's schema, never from the answer.
            answer = getattr(__namespace, leaf)(*params)
            if type(answer) is not int or not (wait is None or wait):
                return answer
            is_job = job
            if is_job is None:
                is_job = __namespace._client._is_job(f"{__namespace._namespace}.{leaf}")
            if not is_job:
                return answer
            return __namespace._client.wait(
                answer, callback=wait if callable(wait) else None
            )

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
            # A `!name` selector is left out of the match (and of the update),
            # so a selector made only of those has nothing to match on. An empty
            # filter would query the whole collection and act on its first row.
            if selectors and all(v is _q.EXCLUDE for v in selectors.values()):
                raise ValueError(
                    f"selector {list(__selector)!r} has nothing to match on: "
                    "name at least one field without a '!' prefix"
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
                result = run("update", fields)
                action = DBAction.UPDATE
        elif _id not in (None, _q.EXCLUDE):
            if __action not in (DBAction.UPDATE, DBAction.UPSERT):
                raise FileExistsError(_id)
            exclude = (idkey, *(opts.get("update_exclude") or []))
            # Drop a field only when it is a selector the record already
            # matches, or a `!` selector. `selectors.get(name)` alone read a
            # non-selector as `None`, which silently dropped every field being
            # set TO None -- a nullable field could never be cleared.
            fields = {
                name: val
                for name, val in fields.items()
                if name not in exclude
                and not (
                    name in selectors
                    and (selectors[name] is _q.EXCLUDE or selectors[name] == val)
                )
            }

            if not force:
                if not current:
                    current = _ty.cast(dict[str, object], __namespace._get(_id))
                if not current:
                    # Without this the miss surfaced as `AttributeError: 'NoneType'
                    # object has no attribute 'get'` from diff(), naming neither
                    # the record nor the collection.
                    raise FileNotFoundError(
                        f"{__namespace._namespace}: no record with {idkey}={_id!r}"
                    )
                fields = _q.diff(current, fields)

            if fields:
                result = run("update", _id, fields)
                action = DBAction.UPDATE
            else:
                result = None

            if result == _id:
                result = __namespace._get(_id)
            elif result is None:
                result = __namespace._get(_id) if not current else current
        else:
            if __action not in (DBAction.CREATE, DBAction.UPSERT):
                raise FileNotFoundError(selectors)
            exclude = (idkey, *(opts.get("create_exclude") or []))
            fields = {name: val for name, val in fields.items() if name not in exclude}
            try:
                result = run("create", fields)
            except _connection.ValidationErrors as e:
                if "already exists" in e.error:
                    raise FileExistsError(e.error)
                else:
                    raise e
            action = DBAction.CREATE

        result = _ty.cast(_T, result)

        if callable(callback):
            callback(action, _id, result)

        return result


class _LoggedArgs:
    """A call's arguments as a log record renders them: redacted, and only
    when the record is actually emitted."""

    __slots__ = ("method", "args")

    def __init__(self, method: str, args: tuple) -> None:
        self.method, self.args = method, args

    def __str__(self) -> str:
        return repr(_auth.redact_call_args(self.method, self.args))


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

    def __repr__(self) -> str:
        # `name` rather than the connection URI: the short label, and
        # credential-free by construction. A traceback renders this repr.
        host = getattr(self._client, "name", None) or self._client
        return f"{self.__class__.__name__}({host}/{self._namespace.replace('.','/')})"

    def __str__(self) -> str:
        return self._namespace

    def __call__(
        self,
        *args,
        _retries=1,
        _method: _ty.Optional[str] = None,
        _ioerror=False,
        _filetransfer: _ty.Union[bool, bytes] = False,
        _timeout: "_ty.Optional[_ty.Union[float, _Unset]]" = _UNSET,
        **kwds,
    ):
        """Invoke this namespace's middleware method.

        ``_retries`` is the number of retries on a new connection after a
        dropped one, made only when the request was never sent
        (:class:`~pytruenas.ConnectionClosed` with ``sent=False``); with the
        default 1 the call is attempted up to twice. ``_timeout`` is
        the per-call timeout in seconds; the default sentinel uses the
        client's configured timeout, ``None`` waits indefinitely. ``_method``
        appends a leaf method name, ``_ioerror`` maps a middleware error to the
        matching ``OSError``, and ``_filetransfer`` routes through
        upload/download.

        ``job=True``, as in the upstream client, waits for the job the method
        starts and returns the job's result (:meth:`TrueNASClient.wait`): a
        failed job raises :class:`~pytruenas.JobFailed`. The wait has no
        deadline unless ``_timeout`` is given. ``job="RETURN"`` returns the
        job id. Any other keyword raises ``TypeError``: middleware methods take
        positional parameters.
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

        job = kwds.pop("job", False)
        call_options = {} if _timeout is _UNSET else {"timeout": _timeout}

        # Middleware methods take POSITIONAL parameters: a dropped
        # `filters=` would query every row, and that answer then drives an
        # update.
        stray = sorted(kwds)
        if stray:
            raise TypeError(
                f"{method}: middleware methods take positional parameters only; "
                f"got keyword(s) {', '.join(stray)}. Pass them in order, e.g. "
                f"query([['uid', '=', 0]]), or use the _query/_get helpers."
            )

        # One initial attempt plus `_retries` reconnect retries after an aborted
        # connection. The loop ends in a result or a raise, never None: a None
        # reads as "no result" and, via _get, turns an upsert into a create.
        attempts = max(0, _retries) + 1
        last_exc: "_ty.Optional[_connection.ClientException]" = None
        for attempt in range(attempts):
            conn = None
            try:
                # Lazy and redacted: the args carry passwords, API keys and
                # private keys (auth.login, install_sshcreds), and formatting
                # them on every call cost time even with TRACE off.
                self._client.logger.log(
                    _TRACE,
                    "Calling method: %s args: %s",
                    method,
                    _LoggedArgs(method, args),
                )
                conn = self._client.conn
                result = conn.call(method, *args, **call_options)
                break
            except _connection.ClientException as e:
                last_exc = e
                # Only a call the server never received is repeated: one lost
                # after it was sent may already have run, and replaying a
                # create, delete or job start is not this layer's call.
                unsent = getattr(e, "sent", True) is False
                if unsent and attempt < attempts - 1:
                    self._client.logger.warning(
                        "Websocket connection was closed, trying again with new connection"
                    )
                    self._client._drop_conn(conn)
                    _time.sleep(1)
                    continue
                raise (ioerror(e) if _ioerror else e) from None
        else:
            # Unreachable: the last attempt raises rather than continuing.
            assert last_exc is not None
            raise ioerror(last_exc) if _ioerror else last_exc

        # `type(...) is int`: a job id. bool is an int subclass, and a method
        # answering True is not job 1.
        if job and job != "RETURN" and type(result) is int:
            try:
                result = self._client.wait(
                    result,
                    timeout=None if isinstance(_timeout, _Unset) else _timeout,
                )
            except _connection.ClientException as e:
                raise (ioerror(e) if _ioerror else e) from None
        return result

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
            child = self._children[name] = Namespace(
                self._client, self._namespace, name
            )
        return child

    def subscribe(
        self,
        __callback: "_ty.Optional[_ty.Callable[[_connection.Event], object]]" = None,
        *,
        event: "_ty.Optional[str]" = None,
        maxsize: int = _connection.DEFAULT_EVENT_QUEUE_SIZE,
    ) -> "_connection.Subscription":
        """Subscribe to this namespace's collection events.

        ``client.api.alert.list.subscribe()`` subscribes to the ``alert.list``
        event -- the event name defaults to this namespace's dotted path.
        Returns a :class:`~pytruenas.connection.Subscription`; consume it via its
        ``events()`` iterator and/or the optional ``__callback`` (invoked inline
        on the reader thread -- keep it fast).

        Pass ``event=`` to subscribe to a different event name than the
        namespace path (e.g. from ``client.api`` root). This is a real method,
        so it shadows any middleware method literally named ``subscribe``; reach
        such a method via ``ns(_method="subscribe", ...)`` if ever needed.
        """
        name = event or self._namespace
        if not name:
            raise ValueError(
                "no event name: call subscribe() on a namespace "
                "(client.api.alert.list.subscribe()) or pass event=..."
            )
        return self._client.conn.subscribe(name, __callback, maxsize=maxsize)

    def _query(self, *__opts: _ty.Union[dict, _q.Option], **filter):
        opts = _q.Option.options(*__opts)
        filter = _q.filter_from_kwargs(**filter)
        return _ty.cast(list[dict[str, object]], self.query(filter, opts))

    def _get(
        self,
        __id_or_filter: _ty.Optional[
            _ty.Union[_ty.Mapping, int, str, _q._Exclude]
        ] = None,
        **__filter,
    ) -> _ty.Optional[dict[str, object]]:
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
        __callback: _ty.Optional[
            _ty.Union[
                _ty.Callable[[DBAction, _ty.Union[str, int], dict[str, object]], None],
                dict,
                _q.Option,
                _ty.Tuple[str, object],
            ]
        ] = None,
        *__opts: _ty.Union[dict, _q.Option, _ty.Tuple[str, object]],
        **__fields,
    ):
        opts = [*__opts]
        if callable(__callback):
            opts.append(("callback", __callback))
        elif __callback:
            opts.append(__callback)

        return DBAction.UPSERT.execute(self, __selector, *opts, **__fields)

    def _update(
        self,
        __selector: _DBSelector = None,
        *__opts: _ty.Union[dict, _q.Option, _ty.Tuple[str, object]],
        **__fields,
    ):
        return DBAction.UPDATE.execute(self, __selector, *__opts, **__fields)

    def _create(
        self,
        *__opts: _ty.Union[dict, _q.Option, _ty.Tuple[str, object]],
        **__fields,
    ):
        return DBAction.CREATE.execute(self, _q.EXCLUDE, *__opts, **__fields)


__all__ = ["Namespace", "DBAction", "ioerror"]
