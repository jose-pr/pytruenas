"""The errors pytruenas raises at run time, all under :class:`TrueNASError`.

``except pytruenas.TrueNASError`` catches every one of them; each is exported
from :mod:`pytruenas`.

* :class:`ClientException` -- a call the middleware failed; ``errno`` carries
  its error number when it has one. Its subclasses:
  :class:`ValidationErrors` (the arguments, per field; also a ``ValueError``),
  :class:`CallTimeout`, :class:`ConnectionClosed` and :class:`JobFailed`.
* :class:`ConnectError` -- the websocket could not be opened: the HTTP upgrade
  was refused or the handshake failed. The websocket library's exception is
  its ``__cause__``.
* :class:`AuthenticationError` -- a login was refused.
* :class:`APIDumpError` -- the API definition could not be fetched intact.
* :class:`UnknownMethod`, :class:`FieldError` -- a method name or a
  ``--field=value`` the API definition does not accept.

None derives ``OSError``, ``TimeoutError`` or ``ConnectionError``: path code
reads any ``OSError`` from ``exists()`` or ``is_dir()`` as "not there", so a
timeout would pass for a missing file. A caller's mistake -- an unknown
keyword, a malformed connection string -- is a plain ``TypeError`` or
``ValueError``. An ``OSError`` that already describes a failure (a refused
port, an unresolvable host, a TLS error) is raised as it is.
"""

from __future__ import annotations

import errno as _errno
import typing as _ty

__all__ = [
    "TrueNASError",
    "ClientException",
    "ValidationErrors",
    "JobFailed",
    "CallTimeout",
    "ConnectionClosed",
    "ConnectError",
    "AuthenticationError",
    "APIDumpError",
    "UnknownMethod",
    "FieldError",
]


class TrueNASError(Exception):
    """Base class of every error pytruenas raises at run time."""


class ClientException(TrueNASError):
    """A middleware call failed, or the connection behind it did.

    ``errno`` carries the middleware's error number when it maps to a POSIX
    errno (used by the filesystem layer to raise the right ``OSError``);
    ``trace``/``extra`` carry the server-side traceback and per-field error
    detail when present.
    """

    def __init__(
        self,
        error: str,
        errno: "_ty.Optional[int]" = None,
        trace: "_ty.Optional[object]" = None,
        extra: "_ty.Optional[list]" = None,
    ) -> None:
        super().__init__(error)
        self.error = error
        self.errno = errno
        self.trace = trace
        self.extra = extra

    def __str__(self) -> str:
        return self.error


class ValidationErrors(ClientException, ValueError):
    """The server rejected a call's arguments, per attribute.

    Each entry of ``errors`` is ``(attribute, errmsg, errcode)``. The string
    form lists every attribute and message, as the middleware reports them.
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


class JobFailed(ClientException):
    """A middleware job ended in ``FAILED`` or ``ABORTED``.

    ``job`` is the job record from ``core.get_jobs`` (``error``,
    ``exception``, ``exc_info``, ...); ``errno`` comes from ``exc_info`` when
    the middleware reports one.
    """

    def __init__(self, job: dict) -> None:
        info = job.get("exc_info") or {}
        super().__init__(
            job.get("error") or f"job {job.get('id')} {job.get('state', '').lower()}",
            info.get("errno"),
            job.get("exception"),
            info.get("extra"),
        )
        self.job = job


class CallTimeout(ClientException):
    """A call did not return within its timeout."""

    def __init__(self) -> None:
        super().__init__("Call timeout", _errno.ETIMEDOUT)


class ConnectionClosed(ClientException):
    """The connection closed before a call's response arrived.

    ``errno`` is ``ECONNABORTED``. ``sent`` says whether the request had been
    written to the socket: ``False`` means the server never saw it and the
    call can safely be made again; ``True`` means the server may have run it
    -- a create, a delete, a job start -- and only the caller knows whether
    repeating it is safe.
    """

    def __init__(self, sent: bool) -> None:
        super().__init__("Connection closed", _errno.ECONNABORTED)
        self.sent = sent


class ConnectError(TrueNASError):
    """The websocket could not be opened: the upgrade or handshake failed.

    ``status`` is the HTTP status the server answered the upgrade with (404
    for a wrong API path), or ``None``. The websocket library's exception is
    the ``__cause__``.
    """

    def __init__(self, message: str, status: "_ty.Optional[int]" = None) -> None:
        super().__init__(message)
        self.status = status


class AuthenticationError(TrueNASError):
    """A login was refused.

    ``response_type`` is the server's discriminator (``AUTH_ERR``/``DENIED``/
    ``EXPIRED``/...); ``response`` is the full response dict for callers that
    need the detail (e.g. a ``REDIRECT`` target). A refused legacy login --
    whose only answer is ``False`` -- is ``AUTH_ERR`` with ``{"method": ...}``.
    """

    def __init__(
        self, response_type: str, response: dict, method: str = "login_ex"
    ) -> None:
        super().__init__(f"{method} failed: {response_type}")
        self.response_type = response_type
        self.response = response


class APIDumpError(TrueNASError, RuntimeError):
    """The API definition could not be fetched or did not survive the trip."""


class UnknownMethod(TrueNASError, LookupError):
    """No such method in this API definition."""


class FieldError(TrueNASError, ValueError):
    """A field name or value the schema does not accept."""
