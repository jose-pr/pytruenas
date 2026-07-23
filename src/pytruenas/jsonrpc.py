"""A lean synchronous JSON-RPC 2.0 client for the TrueNAS middleware.

This is a deliberately small client covering exactly what ``pytruenas`` needs:
open a websocket to the middleware, send a request, wait for the matching
response, and surface errors as exceptions. Jobs are not tracked client-side --
the middleware's own ``core.job_wait`` method (a normal blocking call) is used
for that. Event subscriptions (``core.subscribe``) ARE supported: see
:meth:`Client.subscribe` and :class:`Subscription` -- a bounded queue drained on
the caller's thread, with optional inline callbacks.

Three transports are supported by :class:`Client`:

* ``wss://host/api/current`` -- TLS websocket to a remote host;
* ``ws://host/api/current`` -- plain websocket to a remote host;
* ``ws+unix:///var/run/middleware/middlewared.sock`` -- the local middleware
  unix socket, used when running *on* the NAS (no network round trip, no auth
  needed for a root-owned socket).

The wire format is `JSON-RPC 2.0 <https://www.jsonrpc.org/specification>`_ with
TrueNAS's extended-JSON value encoding (``ejson`` below: ``datetime``/``date``/
``time``/``set``/IP-interface round-tripping).

All annotations use quoted unions so the module imports on Python 3.9.
"""

from __future__ import annotations

import calendar as _calendar
import errno as _errno
import json as _json
import logging as _logging
import os as _os
import queue as _queue
import socket as _socket
import ssl as _ssl
import threading as _threading
import typing as _ty
import uuid as _uuid
from datetime import date as _date
from datetime import datetime as _datetime
from datetime import time as _time
from datetime import timedelta as _timedelta
from datetime import timezone as _timezone
from ipaddress import IPv4Interface as _IPv4Interface
from ipaddress import IPv6Interface as _IPv6Interface

import websocket as _websocket

_LOGGER = _logging.getLogger("pytruenas.jsonrpc")

__all__ = [
    "Client",
    "ClientException",
    "ValidationErrors",
    "CallTimeout",
    "CALL_TIMEOUT",
    "Event",
    "Subscription",
    "dumps",
    "loads",
]

#: Default bound on a subscription's event queue. A slow consumer that lets the
#: queue fill has its OLDEST event dropped (and ``Subscription.dropped``
#: incremented) rather than blocking the shared reader thread.
DEFAULT_EVENT_QUEUE_SIZE = 1000

#: Default per-call timeout in seconds (overridable via ``CALL_TIMEOUT`` env var).
CALL_TIMEOUT = int(_os.environ.get("CALL_TIMEOUT", 60))

#: Default local middleware unix socket (used when the target is local).
DEFAULT_UNIX_SOCKET = "/var/run/middleware/middlewared.sock"

_UNIX_PREFIX = "ws+unix://"


class _Unset:
    """Sentinel type for "timeout not supplied" (distinct from ``None``)."""


#: Marks ``call(timeout=...)`` as "use the client default". ``None`` is a real
#: value meaning "wait indefinitely" (long jobs via ``core.job_wait``), so it
#: cannot double as the default.
_UNSET = _Unset()

#: Compatibility kwargs the upstream client accepts that this lean, synchronous
#: client simply ignores (it does not track jobs client-side).
_COMPAT_KWARGS = frozenset({"job", "background", "callback", "register_call", "raise_"})

# JSON-RPC 2.0 + TrueNAS custom error codes.
_INVALID_PARAMS = -32602
_TRUENAS_CALL_ERROR = -32001


# --------------------------------------------------------------------------
# Extended JSON (ejson): datetime/date/time/set/IP round-tripping
# --------------------------------------------------------------------------


class _EJSONEncoder(_json.JSONEncoder):
    """JSON encoder that also serializes the middleware's extended types."""

    def default(self, obj):
        if isinstance(obj, _datetime):
            return {"$date": int(_calendar.timegm(obj.utctimetuple()) * 1000 + obj.microsecond // 1000)}
        if isinstance(obj, _date):
            return {"$type": "date", "$value": obj.strftime("%Y-%m-%d")}
        if isinstance(obj, _time):
            return {"$time": obj.strftime("%H:%M:%S")}
        if isinstance(obj, set):
            return {"$set": list(obj)}
        if isinstance(obj, _IPv4Interface):
            return {"$ipv4_interface": str(obj)}
        if isinstance(obj, _IPv6Interface):
            return {"$ipv6_interface": str(obj)}
        return super().default(obj)


def _object_hook(obj: dict):
    """Decode the middleware's extended-JSON wrapper objects back to Python."""
    if len(obj) == 1:
        if "$date" in obj:
            ms = obj["$date"]
            return _datetime.fromtimestamp(ms / 1000, tz=_timezone.utc) + _timedelta(
                milliseconds=ms % 1000
            )
        if "$time" in obj:
            return _time(*[int(i) for i in obj["$time"].split(":")[:4]])
        if "$set" in obj:
            return set(obj["$set"])
        if "$ipv4_interface" in obj:
            return _IPv4Interface(obj["$ipv4_interface"])
        if "$ipv6_interface" in obj:
            return _IPv6Interface(obj["$ipv6_interface"])
    elif len(obj) == 2 and obj.get("$type") == "date" and "$value" in obj:
        return _date(*[int(i) for i in obj["$value"].split("-")])
    return obj


def dumps(obj, **kwargs) -> str:
    """Serialize ``obj`` to a JSON string, extended-type aware."""
    return _json.dumps(obj, cls=_EJSONEncoder, **kwargs)


def loads(data: "str | bytes | bytearray", **kwargs):
    """Deserialize a JSON string, decoding the middleware's extended types."""
    return _json.loads(data, object_hook=_object_hook, **kwargs)


# --------------------------------------------------------------------------
# Exceptions
# --------------------------------------------------------------------------


class ClientException(Exception):
    """Any error surfaced by a :class:`Client` call or connection.

    ``errno`` carries the middleware's error number when it maps to a POSIX
    errno (used by the filesystem layer to raise the right ``OSError``);
    ``trace``/``extra`` carry the server-side traceback and per-field error
    detail when present.
    """

    def __init__(
        self,
        error: str,
        errno: "int | None" = None,
        trace: "object | None" = None,
        extra: "list | None" = None,
    ) -> None:
        super().__init__(error)
        self.error = error
        self.errno = errno
        self.trace = trace
        self.extra = extra

    def __str__(self) -> str:
        return self.error


class ValidationErrors(ClientException):
    """A collection of per-attribute validation errors from the server.

    Each entry is ``(attribute, errmsg, errcode)``. The stringified form lists
    every attribute + message, matching how the middleware reports them.
    """

    def __init__(self, errors: "_ty.Iterable") -> None:
        self.errors = [tuple(e) for e in errors]
        super().__init__(str(self))

    def __str__(self) -> str:
        msgs = []
        for attribute, errmsg, errcode in self.errors:
            name = _errno.errorcode.get(errcode, "EUNKNOWN")
            msgs.append(f"[{name}] {attribute or 'ALL'}: {errmsg}")
        return "\n".join(msgs)


class CallTimeout(ClientException):
    """Raised when a call does not return within its timeout."""

    def __init__(self) -> None:
        super().__init__("Call timeout", _errno.ETIMEDOUT)


def _parse_error(error: dict) -> ClientException:
    """Turn a JSON-RPC error object into the appropriate exception."""
    code = error.get("code")
    data = error.get("data")
    if code == _INVALID_PARAMS and isinstance(data, dict) and "extra" in data:
        return ValidationErrors(data["extra"])
    if code == _TRUENAS_CALL_ERROR and isinstance(data, dict):
        return ClientException(
            data.get("reason") or "Call error",
            data.get("error"),
            data.get("trace"),
            data.get("extra"),
        )
    return ClientException(error.get("message") or (data if isinstance(data, str) else str(code)))


# --------------------------------------------------------------------------
# Event subscriptions
# --------------------------------------------------------------------------


class Event(_ty.NamedTuple):
    """One ``collection_update`` notification delivered to a subscription.

    Mirrors the middleware wire shape verified against TrueNAS 26.0:
    ``{"method": "collection_update", "params": {"msg": ..., "collection":
    ..., "fields": {...}}}``.

    * ``collection`` -- the event name subscribed to (the routing key);
    * ``msg`` -- ``"added"`` / ``"changed"`` / ``"removed"``;
    * ``fields`` -- the record payload (may be ``None`` for some events);
    * ``id`` -- the record id when the middleware includes one, else ``None``.
    """

    collection: str
    msg: str
    fields: "dict | None"
    id: "object | None" = None


#: Sentinel put on a subscription's queue to wake a blocked ``events()``
#: iterator when the connection closes.
_EVENT_CLOSED = object()


class Subscription:
    """A live subscription to a middleware event (``core.subscribe``).

    Obtain one from :meth:`Client.subscribe`. Consume events by iterating
    :meth:`events` (a bounded queue drains on the caller's thread -- no hidden
    threads, backpressure is visible) and/or by passing a ``callback`` at
    subscribe time (invoked inline on the reader thread -- keep it fast and
    non-blocking; a raising callback is logged and swallowed so it never kills
    the reader or other subscriptions).

    Close with :meth:`unsubscribe` or a ``with`` block. When the queue fills
    (a slow consumer) the OLDEST event is dropped and :attr:`dropped` is
    incremented -- the reader never blocks.
    """

    __slots__ = ("event", "id", "dropped", "_queue", "_callback", "_client", "_closed")

    def __init__(
        self,
        event: str,
        callback: "_ty.Callable[[Event], object] | None",
        maxsize: int,
        client: "Client",
    ) -> None:
        self.event = event
        self.id: "str | None" = None  # set by Client.subscribe after core.subscribe
        self.dropped = 0
        self._queue: "_queue.Queue" = _queue.Queue(maxsize=maxsize)
        self._callback = callback
        self._client = client
        self._closed = False

    # -- reader side (called on the reader thread) --------------------------

    def _deliver(self, event: "Event") -> None:
        """Route one event to the queue (+ callback). Never blocks/raises."""
        try:
            self._queue.put_nowait(event)
        except _queue.Full:
            # Drop the oldest to make room; count it so a consumer can tell it
            # fell behind. Best-effort -- a concurrent get() may have drained it.
            try:
                self._queue.get_nowait()
                self.dropped += 1
            except _queue.Empty:  # pragma: no cover - race window
                pass
            try:
                self._queue.put_nowait(event)
            except _queue.Full:  # pragma: no cover - race window
                self.dropped += 1
        if self._callback is not None:
            try:
                self._callback(event)
            except Exception:  # a bad callback must not kill the reader
                _LOGGER.warning(
                    "event callback for %r raised; continuing", self.event,
                    exc_info=True,
                )

    def _close(self) -> None:
        """Wake a blocked ``events()`` consumer (connection closed/unsubscribed)."""
        self._closed = True
        try:
            self._queue.put_nowait(_EVENT_CLOSED)
        except _queue.Full:  # pragma: no cover - drop one to make room for the sentinel
            try:
                self._queue.get_nowait()
                self._queue.put_nowait(_EVENT_CLOSED)
            except Exception:
                pass

    # -- consumer side ------------------------------------------------------

    def events(self, timeout: "float | None" = None) -> "_ty.Iterator[Event]":
        """Yield events until the subscription (or the connection) closes.

        Blocks on each event up to ``timeout`` seconds; ``timeout=None`` waits
        indefinitely. The iterator ends cleanly when :meth:`unsubscribe` is
        called or the connection drops.
        """
        while True:
            if self._closed and self._queue.empty():
                return
            try:
                item = self._queue.get(timeout=timeout)
            except _queue.Empty:
                return  # timed out with nothing pending
            if item is _EVENT_CLOSED:
                return
            yield item

    def unsubscribe(self) -> None:
        """Cancel this subscription (idempotent; safe after the client closes)."""
        self._client._unsubscribe(self)

    def __enter__(self) -> "Subscription":
        return self

    def __exit__(self, *exc) -> None:
        self.unsubscribe()


# --------------------------------------------------------------------------
# Client
# --------------------------------------------------------------------------


class Client:
    """A synchronous JSON-RPC 2.0 client for the TrueNAS middleware.

    ``uri`` may be a ``ws://``/``wss://`` URL or a ``ws+unix://`` unix-socket
    URL; ``None`` (or a bare ``ws+unix://``) connects to the local middleware
    socket at :data:`DEFAULT_UNIX_SOCKET`.

    The connection is a single blocking websocket. :meth:`call` sends one
    request and blocks on the matching response (by ``id``); a background
    reader thread demultiplexes responses so concurrent calls from different
    threads are safe, and routes ``collection_update`` notifications to any
    :meth:`subscribe` sinks. Job tracking is intentionally omitted -- use the
    middleware's ``core.job_wait`` for jobs.
    """

    def __init__(
        self,
        uri: "str | None" = None,
        *,
        verify_ssl: bool = True,
        call_timeout: float = CALL_TIMEOUT,
        py_exceptions: bool = False,
    ) -> None:
        if not uri or uri == _UNIX_PREFIX:
            uri = _UNIX_PREFIX + DEFAULT_UNIX_SOCKET
        self.uri = uri
        self.verify_ssl = verify_ssl
        self.call_timeout = call_timeout
        # Accepted for parity with the upstream client; this lean client never
        # asks the server to pickle exceptions.
        self.py_exceptions = py_exceptions

        self._closed = _threading.Event()
        self._send_lock = _threading.Lock()
        self._pending: "dict[str, _Pending]" = {}
        self._pending_lock = _threading.Lock()
        # Event subscriptions, keyed by event name (the notification's
        # ``params.collection`` -- the routing key, verified against live 26.0).
        # A value is a LIST of sinks so two independent subscribers to the same
        # collection both receive it.
        self._subs: "dict[str, list[Subscription]]" = {}
        self._subs_lock = _threading.Lock()

        self._ws = self._connect()
        self._reader = _threading.Thread(target=self._read_loop, daemon=True)
        self._reader.start()

    # -- connection ---------------------------------------------------------

    def _connect(self) -> "_websocket.WebSocket":
        if self.uri.startswith(_UNIX_PREFIX):
            path = self.uri[len(_UNIX_PREFIX) :]
            sock = _socket.socket(_socket.AF_UNIX, _socket.SOCK_STREAM)
            sock.connect(path)
            ws = _websocket.WebSocket()
            # A dummy hostname is used for the HTTP upgrade over the unix
            # socket, per the middleware docs.
            ws.connect("ws://localhost/api/current", socket=sock)
            return ws

        sslopt = None if self.verify_ssl else {"cert_reqs": _ssl.CERT_NONE}
        ws = _websocket.WebSocket(sslopt=sslopt)
        ws.connect(self.uri)
        return ws

    # -- reader -------------------------------------------------------------

    def _read_loop(self) -> None:
        while not self._closed.is_set():
            try:
                raw = self._ws.recv()
            except Exception:
                break
            if not raw:
                break
            try:
                message = loads(raw)
            except Exception:
                continue
            if not isinstance(message, dict):
                continue
            mid = message.get("id")
            if mid is None:
                # A JSON-RPC notification. The middleware sends
                # ``collection_update`` for subscribed events; route it to the
                # matching sinks (keyed by ``params.collection``) or drop it.
                self._route_notification(message)
                continue
            with self._pending_lock:
                pending = self._pending.pop(mid, None)
            if pending is not None:
                pending.resolve(message)
        # Connection ended: fail every waiter so no call blocks forever, and
        # wake every subscription's events() consumer.
        self._closed.set()
        with self._pending_lock:
            pending_calls = list(self._pending.values())
            self._pending.clear()
        for pending in pending_calls:
            pending.fail(ClientException("Connection closed", _errno.ECONNABORTED))
        with self._subs_lock:
            sinks = [s for sinks in self._subs.values() for s in sinks]
            self._subs.clear()
        for sink in sinks:
            sink._close()

    def _route_notification(self, message: dict) -> None:
        """Deliver a ``collection_update`` notification to its subscriptions."""
        if message.get("method") != "collection_update":
            _LOGGER.debug("ignoring notification method %r", message.get("method"))
            return
        params = message.get("params") or {}
        collection = params.get("collection")
        with self._subs_lock:
            sinks = list(self._subs.get(collection, ()))
        if not sinks:
            _LOGGER.debug("no subscription for event %r; dropping", collection)
            return
        event = Event(
            collection=collection,
            msg=params.get("msg"),
            fields=params.get("fields"),
            id=params.get("id"),
        )
        for sink in sinks:
            sink._deliver(event)

    # -- calls --------------------------------------------------------------

    def call(
        self,
        method: str,
        *params,
        timeout: "float | None | _Unset" = _UNSET,
        **_ignored,
    ):
        """Call ``method`` with ``params`` and return its result.

        Blocks until the response arrives or ``timeout`` seconds elapse. The
        default sentinel uses :attr:`call_timeout`; an explicit ``timeout=None``
        waits **indefinitely** (used by ``core.job_wait`` for long jobs).
        Compatibility keyword arguments (``job``, ``background``, ``callback``,
        …) accepted by the upstream client are ignored -- this client is
        synchronous and does not track jobs client-side. Any *other* unexpected
        keyword is logged at debug level rather than silently swallowed.

        Raises :class:`ValidationErrors`/:class:`ClientException` on a server
        error, :class:`CallTimeout` on timeout, and :class:`ClientException`
        with ``errno=ECONNABORTED`` if the connection dropped.
        """
        unexpected = [k for k in _ignored if k not in _COMPAT_KWARGS]
        if unexpected:
            _LOGGER.debug("call(%s): ignoring unexpected kwargs %s", method, unexpected)

        if self._closed.is_set():
            raise ClientException("Connection closed", _errno.ECONNABORTED)

        call_id = str(_uuid.uuid4())
        pending = _Pending()
        with self._pending_lock:
            self._pending[call_id] = pending

        request = {
            "jsonrpc": "2.0",
            "method": method,
            "id": call_id,
            "params": list(params),
        }
        try:
            with self._send_lock:
                self._ws.send(dumps(request))
        except Exception as exc:
            with self._pending_lock:
                self._pending.pop(call_id, None)
            raise ClientException(
                f"Failed to send request: {exc}", _errno.ECONNABORTED
            ) from exc

        wait_timeout = self.call_timeout if isinstance(timeout, _Unset) else timeout
        message = pending.wait(wait_timeout)
        if message is None:
            # Only reachable with a finite timeout; timeout=None waits forever.
            with self._pending_lock:
                self._pending.pop(call_id, None)
            raise CallTimeout()

        if "error" in message and message["error"] is not None:
            raise _parse_error(message["error"])
        return message.get("result")

    # -- subscriptions ------------------------------------------------------

    def subscribe(
        self,
        event: str,
        callback: "_ty.Callable[[Event], object] | None" = None,
        *,
        maxsize: int = DEFAULT_EVENT_QUEUE_SIZE,
    ) -> "Subscription":
        """Subscribe to a middleware event and return a :class:`Subscription`.

        ``event`` is a collection name (e.g. ``"alert.list"``,
        ``"reporting.realtime"``). Consume via the returned subscription's
        :meth:`~Subscription.events` iterator and/or an optional ``callback``
        (called inline on the reader thread -- keep it fast).

        Registers the sink BEFORE issuing ``core.subscribe`` so no event can
        arrive between the server acknowledging and the sink existing; the sink
        is removed again if the subscribe call fails.
        """
        sub = Subscription(event, callback, maxsize, self)
        with self._subs_lock:
            self._subs.setdefault(event, []).append(sub)
        try:
            sub.id = self.call("core.subscribe", event)
        except Exception:
            with self._subs_lock:
                sinks = self._subs.get(event)
                if sinks and sub in sinks:
                    sinks.remove(sub)
                    if not sinks:
                        self._subs.pop(event, None)
            raise
        return sub

    def _unsubscribe(self, sub: "Subscription") -> None:
        """Cancel ``sub`` (idempotent). Called by :meth:`Subscription.unsubscribe`."""
        with self._subs_lock:
            sinks = self._subs.get(sub.event)
            present = bool(sinks and sub in sinks)
            if present:
                sinks.remove(sub)
                if not sinks:
                    self._subs.pop(sub.event, None)
        sub._close()
        if present and sub.id is not None and not self._closed.is_set():
            try:
                self.call("core.unsubscribe", sub.id)
            except Exception:
                # Best-effort: the server drops subscriptions when the socket
                # closes anyway, and a failed unsubscribe must not raise here.
                _LOGGER.debug("core.unsubscribe(%s) failed", sub.id, exc_info=True)

    # -- lifecycle ----------------------------------------------------------

    def close(self) -> None:
        """Close the websocket connection. Idempotent."""
        if self._closed.is_set():
            return
        self._closed.set()
        # Wake any events() consumers; the server drops server-side
        # subscriptions when the socket closes.
        with self._subs_lock:
            sinks = [s for sinks in self._subs.values() for s in sinks]
            self._subs.clear()
        for sink in sinks:
            sink._close()
        try:
            self._ws.close()
        except Exception:
            pass

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, *exc) -> None:
        self.close()


class _Pending:
    """One outstanding call: a threading rendezvous for its response."""

    __slots__ = ("_event", "_message", "_error")

    def __init__(self) -> None:
        self._event = _threading.Event()
        self._message: "dict | None" = None
        self._error: "ClientException | None" = None

    def resolve(self, message: dict) -> None:
        self._message = message
        self._event.set()

    def fail(self, error: ClientException) -> None:
        self._error = error
        self._event.set()

    def wait(self, timeout: float) -> "dict | None":
        if not self._event.wait(timeout):
            return None
        if self._error is not None:
            raise self._error
        return self._message
