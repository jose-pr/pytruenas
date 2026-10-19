"""A lean synchronous JSON-RPC 2.0 client for the TrueNAS middleware.

This is a deliberately small client covering exactly what ``pytruenas`` needs:
open a websocket to the middleware, send a request, wait for the matching
response, and surface errors as exceptions. Jobs are not tracked here: a
job's id is returned, and :meth:`pytruenas.TrueNASClient.wait` polls
``core.get_jobs`` for its outcome (``core.job_wait`` is itself a job and does
not block). Event subscriptions (``core.subscribe``) ARE supported: see
:meth:`TrueNASWSConnection.subscribe` and :class:`Subscription` -- a bounded queue drained on
the caller's thread, with optional inline callbacks.

Three transports are supported by :class:`TrueNASWSConnection`:

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
import math as _math
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
from time import monotonic as _monotonic

import websocket as _websocket

from . import _tls
from .exceptions import (
    CallTimeout,
    ClientException,
    ConnectError,
    ConnectionClosed,
    JobFailed,
    ValidationErrors,
)
from ._utils.io import json_scalar as _json_scalar

_LOGGER = _logging.getLogger("pytruenas.connection")

__all__ = [
    "TrueNASWSConnection",
    "CALL_TIMEOUT",
    "CONNECT_TIMEOUT",
    "default_call_timeout",
    "Event",
    "Subscription",
    "dumps",
    "loads",
]

#: Default bound on a subscription's event queue. A slow consumer that lets the
#: queue fill has its OLDEST event dropped (and ``Subscription.dropped``
#: incremented) rather than blocking the shared reader thread.
DEFAULT_EVENT_QUEUE_SIZE = 1000

#: Per-call timeout in seconds when neither the caller nor
#: ``$PYTRUENAS_CALL_TIMEOUT`` sets one (see :func:`default_call_timeout`).
CALL_TIMEOUT = 60.0

#: Default timeout in seconds for opening the websocket (TCP/unix connect, TLS
#: and the HTTP upgrade). Without one, an unresponsive host blocked forever.
CONNECT_TIMEOUT = 30

#: Default local middleware unix socket (used when the target is local).
DEFAULT_UNIX_SOCKET = "/var/run/middleware/middlewared.sock"

_UNIX_PREFIX = "ws+unix://"


def default_call_timeout() -> float:
    """The per-call timeout a connection gets when it is given none.

    ``$PYTRUENAS_CALL_TIMEOUT`` (seconds, a positive number) when set and not
    empty, else :data:`CALL_TIMEOUT`. Read each time a connection is built,
    never at import. A value that is not a positive number raises
    ``ValueError`` naming the variable.
    """
    from ._utils.env import ENV

    raw = (ENV.get("CALL_TIMEOUT") or "").strip()
    if not raw:
        return CALL_TIMEOUT
    try:
        value = float(raw)
    except ValueError:
        value = _math.nan
    if not (value > 0 and _math.isfinite(value)):
        raise ValueError(
            f"${ENV.prefix}CALL_TIMEOUT is {raw!r}: expected a positive number "
            "of seconds"
        )
    return value


class _Unset:
    """Sentinel type for "timeout not supplied" (distinct from ``None``)."""


#: Marks ``call(timeout=...)`` as "use the client default". ``None`` is a real
#: value meaning "wait indefinitely" (a long-running call), so it
#: cannot double as the default.
_UNSET = _Unset()

#: Reference point for ``$date`` decoding (the middleware sends milliseconds).
_EPOCH = _datetime(1970, 1, 1, tzinfo=_timezone.utc)

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
            return {
                "$date": int(
                    _calendar.timegm(obj.utctimetuple()) * 1000
                    + obj.microsecond // 1000
                )
            }
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

        # Everything above is an EXTENDED type the middleware round-trips
        # through a wrapper object, and must keep its exact shape. What follows
        # is the general fallback for ordinary wrapper values -- an IP address,
        # a MAC, a path, an enum-ish domain type -- which the API just wants as
        # a scalar. Ordering matters: a blanket str() ahead of these would send
        # `"2026-01-01T00:00:00"` where the middleware expects `{"$date": ...}`.
        return _json_scalar(obj, default=super().default)


def _object_hook(obj: dict):
    """Decode the middleware's extended-JSON wrapper objects back to Python."""
    if len(obj) == 1:
        if "$date" in obj:
            # From the epoch, not fromtimestamp() plus the remainder: that
            # counted the sub-second part twice (a .600 timestamp came back
            # 1.2 s late). This is also correct for a negative value.
            return _EPOCH + _timedelta(milliseconds=obj["$date"])
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


def loads(data: "_ty.Union[str, bytes, bytearray]", **kwargs):
    """Deserialize a JSON string, decoding the middleware's extended types."""
    return _json.loads(data, object_hook=_object_hook, **kwargs)


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
    return ClientException(
        error.get("message") or (data if isinstance(data, str) else str(code))
    )


def _handshake_error(uri: str, error: Exception) -> ConnectError:
    """A websocket-client handshake failure as a :class:`ConnectError`."""
    status = getattr(error, "status_code", None)
    message = f"could not open the websocket to {uri}: "
    if status is not None:
        message += f"the server answered the upgrade with HTTP {status}"
    else:
        message += str(error) or type(error).__name__
    return ConnectError(message, status if isinstance(status, int) else None)


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
    fields: "_ty.Optional[dict]"
    id: "_ty.Optional[object]" = None


#: Sentinel put on a subscription's queue to wake a blocked ``events()``
#: iterator when the connection closes.
_EVENT_CLOSED = object()


class Subscription:
    """A live subscription to a middleware event (``core.subscribe``).

    Obtain one from :meth:`TrueNASWSConnection.subscribe`. Consume events by iterating
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
        callback: "_ty.Optional[_ty.Callable[[Event], object]]",
        maxsize: int,
        client: "TrueNASWSConnection",
    ) -> None:
        self.event = event
        self.id: "_ty.Optional[str]" = (
            None  # set by TrueNASWSConnection.subscribe after core.subscribe
        )
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
                self._client.logger.warning(
                    "event callback for %r raised; continuing",
                    self.event,
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

    def events(self, timeout: "_ty.Optional[float]" = None) -> "_ty.Iterator[Event]":
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
# TrueNASWSConnection
# --------------------------------------------------------------------------


class TrueNASWSConnection:
    """A synchronous JSON-RPC 2.0 client for the TrueNAS middleware.

    ``uri`` may be a ``ws://``/``wss://`` URL or a ``ws+unix://`` unix-socket
    URL; ``None`` (or a bare ``ws+unix://``) connects to the local middleware
    socket at :data:`DEFAULT_UNIX_SOCKET`.

    The connection is a single blocking websocket. :meth:`call` sends one
    request and blocks on the matching response (by ``id``); a background
    reader thread demultiplexes responses so concurrent calls from different
    threads are safe, and routes ``collection_update`` notifications to any
    :meth:`subscribe` sinks. Job tracking is intentionally omitted -- use the
    :meth:`pytruenas.TrueNASClient.wait` for jobs.
    """

    def __init__(
        self,
        uri: "_ty.Optional[str]" = None,
        *,
        verify: "_ty.Union[bool, str, _os.PathLike[str], _ssl.SSLContext]" = True,
        call_timeout: "_ty.Optional[_ty.Union[float, _Unset]]" = _UNSET,
        connect_timeout: "_ty.Optional[float]" = CONNECT_TIMEOUT,
        logger: "_ty.Optional[_ty.Union[_logging.Logger, _logging.LoggerAdapter]]" = None,
    ) -> None:
        if not uri or uri == _UNIX_PREFIX:
            uri = _UNIX_PREFIX + DEFAULT_UNIX_SOCKET
        self.uri = uri
        #: TLS verification: see :data:`pytruenas._tls.Verify`.
        self.verify = _tls.check(verify)
        #: Seconds a call waits by default; ``None`` waits indefinitely.
        self.call_timeout: "_ty.Optional[float]" = (
            default_call_timeout() if isinstance(call_timeout, _Unset) else call_timeout
        )
        self.connect_timeout = connect_timeout
        #: Where this connection's records go. A host passes its own
        #: name-bound logger, so "connection was closed" says *which* host
        #: closed even with several open at once; standalone use falls back to
        #: the module logger, which is what this class did unconditionally
        #: before (a module global cannot know its caller's target).
        self.logger = logger if logger is not None else _LOGGER

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
        # Whether the socket has been shut down; separate from `_closed`, which
        # the reader sets on its own, so close() still releases the socket
        # after the server ended the connection. Its own lock: a send blocked
        # on a peer that stopped reading holds `_send_lock`, and the shutdown is
        # what unblocks it.
        self._released = False
        #: Why the reader stopped, when it stopped on an error.
        self._end_cause: "_ty.Optional[BaseException]" = None
        self._release_lock = _threading.Lock()
        # A send is bounded by its call's timeout: `_watch_sends` shuts the
        # socket down when one is still blocked past `_sending_until`.
        self._watch = _threading.Condition()
        self._sending_until: "_ty.Optional[float]" = None
        self._send_timed_out = False
        self._watchdog: "_ty.Optional[_threading.Thread]" = None

        self._open_lock = _threading.Lock()
        self._ws: "_ty.Optional[_websocket.WebSocket]" = None
        self._reader: "_ty.Optional[_threading.Thread]" = None

    def connect(self) -> "TrueNASWSConnection":
        """Open the websocket and start the reader thread; idempotent.

        Blocks for at most ``connect_timeout`` (connect, TLS and the HTTP
        upgrade). A call opens the connection itself if this was not called;
        a closed connection is not reopened (:class:`ConnectionClosed`).
        A refused upgrade or a failed handshake raises :class:`ConnectError`;
        an ``OSError`` (a refused port, an unresolvable host, TLS) is raised
        as it is.
        """
        with self._open_lock:
            if self._ws is None:
                if self._closed.is_set():
                    raise ConnectionClosed(sent=False)
                self._ws = self._connect()
                self._reader = _threading.Thread(target=self._read_loop, daemon=True)
                self._reader.start()
        return self

    # -- connection ---------------------------------------------------------

    def _connect(self) -> "_websocket.WebSocket":
        if self.uri.startswith(_UNIX_PREFIX):
            path = self.uri[len(_UNIX_PREFIX) :]
            sock = _socket.socket(_socket.AF_UNIX, _socket.SOCK_STREAM)
            sock.settimeout(self.connect_timeout)
            sock.connect(path)
            ws = _websocket.WebSocket()
            # A dummy hostname is used for the HTTP upgrade over the unix
            # socket, per the middleware docs.
            try:
                ws.connect(
                    "ws://localhost/api/current",
                    socket=sock,
                    timeout=self.connect_timeout,
                )
            except _websocket.WebSocketException as exc:
                sock.close()
                raise _handshake_error(self.uri, exc) from exc
            ws.settimeout(None)
            return ws

        # The trust decision is shared with every other leg: pytruenas._tls.
        ws = _websocket.WebSocket(sslopt=_tls.sslopt(self.verify))
        try:
            ws.connect(self.uri, timeout=self.connect_timeout)
        except _websocket.WebSocketException as exc:
            ws.shutdown()
            raise _handshake_error(self.uri, exc) from exc
        # websocket-client keeps the connect timeout as the socket's read
        # timeout; the reader blocks on recv() for as long as the connection
        # is idle, so clear it.
        ws.settimeout(None)
        return ws

    # -- reader -------------------------------------------------------------

    def _read_loop(self) -> None:
        try:
            while not self._closed.is_set():
                try:
                    raw = self._ws.recv()
                except Exception as exc:
                    # The cause reaches the log and every waiting call: a
                    # dropped socket otherwise looked like a slow server.
                    self._end_cause = exc
                    if self._closed.is_set():
                        self.logger.debug("connection closed: %s", exc)
                    else:
                        self.logger.warning(
                            "connection lost: %s", exc or type(exc).__name__
                        )
                    break
                if not raw:
                    if not self._closed.is_set():
                        self.logger.warning("connection closed by the server")
                    break
                try:
                    self._dispatch(raw)
                except Exception:
                    # One bad message (a notification of an unexpected shape, a
                    # failing subscription callback) must not kill the reader:
                    # that wedged the connection -- never marked closed, every
                    # call waiting out its timeout.
                    self.logger.warning("dropping a message", exc_info=True)
        finally:
            self._reader_ended()

    def _dispatch(self, raw) -> None:
        try:
            message = loads(raw)
        except Exception as exc:
            # The response DID arrive; only decoding it failed (a malformed
            # `$date`, say). Dropping it left the caller waiting out its whole
            # timeout, so find the id with a plain json.loads and fail that one
            # call instead.
            self.logger.warning("undecodable response: %s", exc)
            self._fail_undecodable(raw, exc)
            return
        if not isinstance(message, dict):
            return
        mid = message.get("id")
        if mid is None:
            # A JSON-RPC notification. The middleware sends
            # ``collection_update`` for subscribed events; route it to the
            # matching sinks (keyed by ``params.collection``) or drop it.
            self._route_notification(message)
            return
        with self._pending_lock:
            pending = self._pending.pop(mid, None)
        if pending is not None:
            pending.resolve(message)

    def _fail_undecodable(self, raw, exc: Exception) -> None:
        """Fail the one call a response belongs to when it cannot be decoded."""
        try:
            plain = _json.loads(raw)
            mid = plain.get("id") if isinstance(plain, dict) else None
        except Exception:
            return
        if mid is None:
            return
        with self._pending_lock:
            pending = self._pending.pop(mid, None)
        if pending is not None:
            pending.fail(ClientException(f"undecodable response: {exc}", _errno.EPROTO))

    def _reader_ended(self) -> None:
        """Connection ended: fail every waiter so no call blocks forever, wake
        every subscription's events() consumer, and release the socket."""
        with self._pending_lock:
            # Set under the lock call() registers under, so no call can slip
            # in between and wait on a reader that is gone.
            self._closed.set()
            pending_calls = list(self._pending.values())
            self._pending.clear()
        for pending in pending_calls:
            error = ConnectionClosed(sent=True)
            error.__cause__ = self._end_cause
            pending.fail(error)
        with self._subs_lock:
            sinks = [s for sinks in self._subs.values() for s in sinks]
            self._subs.clear()
        for sink in sinks:
            sink._close()
        self._release()

    def _route_notification(self, message: dict) -> None:
        """Deliver a ``collection_update`` notification to its subscriptions."""
        if message.get("method") != "collection_update":
            self.logger.debug("ignoring notification method %r", message.get("method"))
            return
        params = message.get("params")
        if not isinstance(params, dict):
            self.logger.debug("ignoring notification without params: %r", message)
            return
        collection = params.get("collection")
        with self._subs_lock:
            sinks = list(self._subs.get(collection, ()))
        if not sinks:
            self.logger.debug("no subscription for event %r; dropping", collection)
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
        timeout: "_ty.Optional[_ty.Union[float, _Unset]]" = _UNSET,
    ):
        """Call ``method`` with ``params`` and return its result.

        Blocks until the response arrives or ``timeout`` seconds elapse. The
        default sentinel uses :attr:`call_timeout`; an explicit ``timeout=None``
        waits **indefinitely** (a long-running call). A job's id is returned:
        ``client.api.<method>(..., job=True)`` waits for the job (see
        :class:`~pytruenas.namespace.Namespace`).

        Raises :class:`ValidationErrors`/:class:`ClientException` on a server
        error, :class:`CallTimeout` on timeout, :class:`ConnectionClosed`
        (``errno=ECONNABORTED``; ``.sent`` says whether the server may have run
        the call) if the connection dropped, and :class:`TypeError` for a
        parameter JSON cannot encode.
        """
        if _threading.current_thread() is self._reader:
            # The reader is the only thread that delivers responses; blocking
            # it on one deadlocked until the call timed out.
            raise RuntimeError(
                f"{method}: cannot make a blocking call from a subscription "
                "callback; consume Subscription.events() on another thread"
            )

        if self._ws is None:
            self.connect()
        call_id = str(_uuid.uuid4())
        # Encoded before anything is registered or sent: a parameter JSON
        # cannot encode is the caller's error, and it was reported as a
        # dropped connection (ECONNABORTED) -- and so retried on a new one.
        try:
            request = dumps(
                {
                    "jsonrpc": "2.0",
                    "method": method,
                    "id": call_id,
                    "params": list(params),
                }
            )
        except (TypeError, ValueError) as exc:
            raise TypeError(
                f"{method}: parameters are not JSON-encodable: {exc}"
            ) from None

        pending = _Pending()
        with self._pending_lock:
            # Checked and registered atomically against _reader_ended/close,
            # which set _closed under this lock: otherwise a call registered
            # just after the reader failed every waiter waited forever.
            if self._closed.is_set():
                raise ConnectionClosed(sent=False)
            self._pending[call_id] = pending

        wait_timeout = self.call_timeout if isinstance(timeout, _Unset) else timeout
        try:
            self._send(request, wait_timeout)
        except Exception as exc:
            with self._pending_lock:
                self._pending.pop(call_id, None)
            if self._send_timed_out:
                # Part of the request may be on the wire: the connection is
                # unusable, and the call may have reached the server.
                self.close()
                raise CallTimeout() from None
            raise ConnectionClosed(sent=False) from exc

        message = pending.wait(wait_timeout)
        if message is None:
            # Only reachable with a finite timeout; timeout=None waits forever.
            with self._pending_lock:
                self._pending.pop(call_id, None)
            raise CallTimeout()

        if "error" in message and message["error"] is not None:
            raise _parse_error(message["error"])
        return message.get("result")

    def _send(self, request: str, timeout: "_ty.Optional[float]") -> None:
        """Send one frame; a send still blocked after ``timeout`` is aborted."""
        assert self._ws is not None
        with self._send_lock:
            if timeout is not None:
                with self._watch:
                    self._sending_until = _monotonic() + timeout
                    if self._watchdog is None:
                        self._watchdog = _threading.Thread(
                            target=self._watch_sends, daemon=True
                        )
                        self._watchdog.start()
                    self._watch.notify()
            try:
                self._ws.send(request)
            finally:
                with self._watch:
                    self._sending_until = None

    def _watch_sends(self) -> None:
        """Shut the socket down under a send blocked past its deadline.

        A peer that stops reading fills the socket buffers, and a blocking
        send then waits forever: the call's timeout covered only the wait for
        the response, and ``close()`` queued behind the send.
        """
        with self._watch:
            while True:
                if self._closed.is_set():
                    return
                until = self._sending_until
                if until is None:
                    self._watch.wait()
                    continue
                left = until - _monotonic()
                if left > 0:
                    self._watch.wait(left)
                    continue
                self._send_timed_out = True
                break
        self._release()

    # -- subscriptions ------------------------------------------------------

    def subscribe(
        self,
        event: str,
        callback: "_ty.Optional[_ty.Callable[[Event], object]]" = None,
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
                self.logger.debug("core.unsubscribe(%s) failed", sub.id, exc_info=True)

    # -- lifecycle ----------------------------------------------------------

    def close(self) -> None:
        """Close the websocket connection. Idempotent.

        Also releases the socket when the reader already ended the connection
        (the server closed it).
        """
        with self._pending_lock:
            was_closed = self._closed.is_set()
            self._closed.set()
        with self._watch:
            self._watch.notify_all()
        if self._ws is None:
            return
        if not was_closed:
            # Wake any events() consumers; the server drops server-side
            # subscriptions when the socket closes.
            with self._subs_lock:
                sinks = [s for sinks in self._subs.values() for s in sinks]
                self._subs.clear()
            for sink in sinks:
                sink._close()
            if not self._send_lock.locked():
                # The close frame, without waiting for the peer's answer as
                # WebSocket.close() does: that wait reads the socket the
                # reader thread is blocked on, so a peer that never answers
                # held close() for good. A blocked send holds the frame lock.
                try:
                    self._ws.send_close()
                except Exception:
                    pass
        self._release()

    def _release(self) -> None:
        """Shut the socket down, once.

        ``shutdown(SHUT_RDWR)`` first: it is what wakes a read or a send
        blocked on the socket in another thread on every platform, where
        closing the descriptor alone does not on Linux.
        """
        with self._release_lock:
            if self._released or self._ws is None:
                return
            self._released = True
        sock = getattr(self._ws, "sock", None)
        if sock is not None:
            try:
                sock.shutdown(_socket.SHUT_RDWR)
            except Exception:
                pass
        try:
            self._ws.shutdown()
        except Exception:
            pass

    def __enter__(self) -> "TrueNASWSConnection":
        return self.connect()

    def __exit__(self, *exc) -> None:
        self.close()


class _Pending:
    """One outstanding call: a threading rendezvous for its response."""

    __slots__ = ("_event", "_message", "_error")

    def __init__(self) -> None:
        self._event = _threading.Event()
        self._message: "_ty.Optional[dict]" = None
        self._error: "_ty.Optional[ClientException]" = None

    def resolve(self, message: dict) -> None:
        self._message = message
        self._event.set()

    def fail(self, error: ClientException) -> None:
        self._error = error
        self._event.set()

    def wait(self, timeout: float) -> "_ty.Optional[dict]":
        if not self._event.wait(timeout):
            return None
        if self._error is not None:
            raise self._error
        return self._message
