"""``hostctl`` integration: the TrueNAS host configuration.

:class:`TrueNASConfig` is the ``hostctl`` :class:`~hostctl.host.HostConfig` for
a TrueNAS middleware target. It carries *parsed* connection settings and nothing
more -- constructing one performs no network I/O, which is what lets a config be
built offline, logged, and round-tripped through its canonical URI.

Scheme handling has two deliberately separate layers:

* **The hostctl registry** sees only ``truenas``/``truenas+auto``/``truenas+ws``/
  ``truenas+wss``/``truenas+unix``. pytruenas does not claim bare ``wss://`` or
  ``https://`` globally -- hostctl is protocol-agnostic, and hijacking a generic
  scheme would risk an "ambiguous host URI matched" collision with any other
  configuration that legitimately wants it.
* **pytruenas' own entry point** additionally understands every connection
  string :class:`~pytruenas.TrueNASClient` has always accepted -- a bare host,
  ``host:port``, ``ws``/``wss``, ``http``/``https``, a unix socket path, or
  ``None`` -- by rewriting it to a ``truenas+*`` URI first. That rewrite is
  :func:`_normalize_target`: one pure string function, no I/O.

The scheme and API path a target leaves out are *defaulted*, not probed: a
remote target with neither resolves to ``wss://<host>/api/<version>``, and only
an explicit ``ws``/``http`` selects plaintext. :attr:`~TrueNASConfig.needs_scheme_probe`
and :attr:`~TrueNASConfig.needs_path_probe` record that the caller did not say,
which is what makes the default visible to a caller that wants to ask the
server itself; nothing in this package performs such a request.
"""

from __future__ import annotations

import copy as _copy
import dataclasses as _dataclasses
import functools as _functools
import inspect as _inspect
import json as _js
import logging as _logging
import os as _os
import re as _re
import ssl as _ssl
import threading as _threading
import typing as _ty
import weakref as _weakref
from functools import cached_property as _cached_property
from urllib.parse import quote as _quote
from urllib.parse import unquote as _unquote
from urllib.parse import urlencode as _urlencode
from urllib.parse import urlsplit as _urlsplit

import requests as _req
from duho import fanout as _fanout
from hostctl import DEFAULT as _DEFAULT
from hostctl import PosixHost as _PosixHost
from hostctl import Timeout
from hostctl import uri_host as _uri_host
from hostctl import uri_hostname as _uri_hostname
from hostctl.host import HostConfig as _HostConfig
from hostctl.uri import strict_uri_query as _strict_uri_query

from . import auth as _auth
from . import connection as _connection
from .connection import DEFAULT_UNIX_SOCKET
from . import namespace as _namespace
from .namespace import Namespace as _Namespace
from . import _tls
from .target import Target as _TGT
from .target import redact as _redact_target

if _ty.TYPE_CHECKING:  # pragma: no cover - typing only
    from hostctl import SSHConfig
    from hostctl.host import Host, HostInfo
    from hostctl.provider import ExecutorProvider, PathProvider
    from truenasapi_typings.current import Current

    #: `TrueNASClient[Current]` types `.api` with the generated stubs.
    ApiVersion = _ty.TypeVar("ApiVersion", bound=_Namespace, default=Current)
else:
    ApiVersion = _ty.TypeVar("ApiVersion", bound=_Namespace)

#: The local middleware unix socket. Re-exported from :mod:`pytruenas.connection`
#: rather than redefined, so the two can never drift apart.
DEFAULT_SOCKET_PATH = DEFAULT_UNIX_SOCKET

#: Scheme meaning "the caller did not say" -- a real registered scheme, not a
#: placeholder, so a config round-trips through its URI. It resolves to wss and
#: the configured API version at connect time (see `needs_scheme_probe`).
AUTO_SCHEME = "truenas+auto"

_SCHEME_PREFIX = "truenas+"

#: Maps every scheme a user may type to its canonical ``truenas+*`` form. http
#: and https collapse onto the websocket transport: the transport is *always* a
#: websocket, and the HTTP(S) side channels (upload/download) derive their URL
#: by mapping back. Keeping two spellings of one transport would duplicate that
#: mapping for no gain.
_SCHEME_ALIASES = {
    "": AUTO_SCHEME,
    "auto": AUTO_SCHEME,
    "ws": "truenas+ws",
    "wss": "truenas+wss",
    "http": "truenas+ws",
    "https": "truenas+wss",
    "ws+unix": "truenas+unix",
    "unix": "truenas+unix",
    "truenas": AUTO_SCHEME,
    "truenas+auto": AUTO_SCHEME,
    "truenas+ws": "truenas+ws",
    "truenas+wss": "truenas+wss",
    "truenas+http": "truenas+ws",
    "truenas+https": "truenas+wss",
    "truenas+unix": "truenas+unix",
}

#: Characters left as written when a socket path is spelled as a URI path:
#: RFC 3986 ``pchar`` plus ``/``. ``?``, ``#``, ``%`` and space are encoded.
_SOCKET_PATH_SAFE = "/:@-._~!$&'()*+,;="

#: Hosts that mean "this machine" -- matching ``Target.is_local`` so the
#: local-socket shortcut behaves exactly as it does today.
_LOCAL_HOSTS = {"", "localhost", "127.0.0.1"}


class _HostLogger(_logging.LoggerAdapter):
    """A logger that prefixes every record with the host it belongs to.

    ``[nas1] Websocket connection was closed`` rather than a bare
    ``Websocket connection was closed`` -- with more than one client open, an
    unattributed record cannot be acted on, and there is no other point in the
    stack that knows both the message and the target.

    An adapter, not a filter: it needs no installation on a handler, so it works
    with whatever logging the caller has already configured (including none),
    and it composes with the CLI's fan-out prefix instead of competing with it
    -- ``duho.fanout`` tags at the handler, this tags at the call site, and a
    record that somehow passed through both would read ``[nas1] [nas1] ...``,
    which :meth:`process` suppresses.
    """

    def process(self, msg, kwargs):
        name = self.extra["name"] if self.extra else ""
        # Inside a duho fan-out over this host, the fan-out's handler filter
        # tags the record with the same name.
        if name and _fanout_label(_fanout.current_target.get()) == name:
            return msg, kwargs
        prefix = f"[{name}] " if name else ""
        text = str(msg)
        if prefix and text.startswith(prefix):
            return text, kwargs
        return f"{prefix}{text}", kwargs


@_functools.lru_cache(maxsize=32)
def _target_name(target: str) -> "str | None":
    try:
        return TrueNASConfig.from_target(target).name
    except Exception:
        return None


def _fanout_label(target: object) -> "str | None":
    """The ``[...]`` prefix a duho fan-out puts on ``target``'s records.

    The CLI fans out over connection strings labelled with the host's name;
    a fan-out with no label prefixes ``str(target)``.
    """
    if target is None:
        return None
    if isinstance(target, str):
        return _target_name(target) or target
    return str(target)


def _without_otp(creds: "_auth.Credentials") -> "_auth.Credentials":
    """``creds`` with its one-time code spent, for a reconnect to repeat.

    The server accepts a code once: replaying it failed the reconnect, and
    ``otp_provider`` was never asked. The caller's object is left as it was.
    """
    if not getattr(creds, "otp", None):
        return creds
    spent = _copy.copy(creds)
    spent.otp = None  # type: ignore[attr-defined]
    return spent


#: A token in a URL's query: what `_side_request` strips from a message.
_TOKEN_IN_QUERY = _re.compile(r"((?:auth_)?token=)[^&#\s'\")]+")


def _transport_cause(exc: BaseException) -> "_ty.Optional[OSError]":
    """The ``OSError`` underneath a ``requests`` connection error, if any.

    ``requests`` wraps urllib3's error, which wraps the socket's or the TLS
    layer's (in ``reason``, ``args[0]`` or the exception chain).
    """
    seen: "set[int]" = set()
    pending: "list[object]" = [exc]
    while pending:
        current = pending.pop(0)
        if not isinstance(current, BaseException) or id(current) in seen:
            continue
        seen.add(id(current))
        module = type(current).__module__.split(".")[0]
        if isinstance(current, OSError) and module not in ("requests", "urllib3"):
            return current
        pending += [
            getattr(current, "reason", None),
            *current.args[:1],
            current.__cause__,
            current.__context__,
        ]
    return None


def _side_channel_error(exc: "_req.RequestException") -> BaseException:
    """What a failed side-channel request raises in place of ``requests``' error.

    The same failure raises the same type as on the API websocket: a TLS or
    socket error is that ``OSError`` (``ssl.SSLError``,
    ``ConnectionRefusedError``, ...), a read that timed out is
    :class:`~pytruenas.exceptions.CallTimeout`, and an HTTP error status a
    :class:`~pytruenas.exceptions.ClientException`. A message never carries
    the token a download link has in its query.
    """
    message = _TOKEN_IN_QUERY.sub(r"\1<redacted>", str(exc))
    if isinstance(exc, _req.ReadTimeout):
        return _connection.CallTimeout()
    if isinstance(exc, _req.ConnectionError):
        cause = _transport_cause(exc)
        if cause is not None:
            return cause
        if isinstance(exc, _req.ConnectTimeout):
            return TimeoutError(message)
        return ConnectionError(message)
    return _connection.ClientException(message)


class PendingDownload:
    """A download the middleware prepared: its ``job_id``, and the bytes on ``fetch()``.

    ``TrueNASClient.download(..., wait=False)`` returns one. The link is
    single-use and carries a token, so it is not shown in the ``repr``.
    """

    def __init__(self, host: "TrueNASClient", job_id: int, uri: str, buffered: bool):
        self.job_id = job_id
        self._host = host
        self._uri = uri
        self._buffered = buffered

    def fetch(
        self, callback: "_ty.Optional[_ty.Callable[..., object]]" = None
    ) -> bytes:
        """The downloaded bytes, once the job that produced them has finished.

        A failed job raises :class:`~pytruenas.connection.JobFailed`. A
        buffered download's job is waited for before the fetch; an unbuffered
        one streams into the response and is checked after it.
        """
        if self._buffered:
            self._host.wait(self.job_id, callback=callback)
        content = self._host._side_request("GET", self._uri).content
        if not self._buffered:
            self._host.wait(self.job_id, callback=callback)
        return content

    def __repr__(self) -> str:
        return f"PendingDownload(job_id={self.job_id!r})"


def _close_quietly(closeable: object) -> None:
    """Close something during garbage collection, where raising is useless."""
    close = getattr(closeable, "close", None)
    if not callable(close):
        return
    try:
        close()
    except Exception:  # pragma: no cover - interpreter teardown
        pass


def _resolve_logger(logger: object, name: "_ty.Optional[str]" = None):
    """A ``Logger`` from a name, an instance, or ``None``.

    When ``name`` is given the result is wrapped in a :class:`_HostLogger` so
    every record it emits identifies the host. An adapter passed in by the
    caller is left alone -- they have already decided how their records look.
    """
    if logger is None:
        resolved: object = _logging.getLogger("pytruenas")
    elif isinstance(logger, str):
        resolved = _logging.getLogger(logger)
    else:
        resolved = logger
    if name and isinstance(resolved, _logging.Logger):
        return _HostLogger(resolved, {"name": name})
    return _ty.cast(_logging.Logger, resolved)


def _asyncssh():
    """Import ``asyncssh`` on demand (the optional ``ssh`` extra)."""
    try:
        import asyncssh
    except ImportError as exc:
        from hostctl import MissingExtraError

        raise MissingExtraError(
            "ssh", "deriving an SSH public key", distribution="pytruenas"
        ) from exc
    return asyncssh


def _public_key(private_key: str) -> str:
    """Derive the OpenSSH public key for ``private_key``.

    Only reached when the public half is genuinely unknown -- a caller who
    passed ``private_key=`` to :meth:`TrueNASClient.install_sshcreds` and nothing
    else. Every other path gets both halves from the middleware, which is what
    keeps ``install_sshcreds`` usable without the optional ``ssh`` extra: it
    provisions a keypair through the API and never opens an SSH connection.

    This is pure key math, so it prefers ``cryptography`` over ``asyncssh``:
    it is what asyncssh itself depends on for the primitives (so the ``ssh``
    extra already brings it), it is far lighter than a whole SSH protocol
    stack, and it is commonly present for unrelated reasons. ``asyncssh``
    remains the fallback, so an environment that has only that keeps working.

    Unlike asyncssh's single entry point, ``cryptography`` needs the loader
    that matches the encoding -- ``load_ssh_private_key`` for an OpenSSH key
    block, ``load_pem_private_key`` for PKCS#8/PEM -- and TrueNAS may hand back
    either, so both are tried before giving up.
    """
    try:
        from cryptography.hazmat.primitives import serialization
    except ImportError:
        return (
            _asyncssh()
            .import_private_key(private_key)
            .export_public_key()
            .decode()
            .strip()
        )

    data = private_key.encode()
    for loader in (
        serialization.load_ssh_private_key,
        serialization.load_pem_private_key,
    ):
        try:
            key = loader(data, password=None)
        except Exception:
            # Wrong encoding for this loader (or a genuinely bad key -- the
            # final raise below reports that, once both have been tried).
            continue
        return (
            key.public_key()
            .public_bytes(
                serialization.Encoding.OpenSSH,
                serialization.PublicFormat.OpenSSH,
            )
            .decode()
            .strip()
        )

    raise ValueError(
        "could not parse the SSH private key: expected an OpenSSH or PEM/PKCS#8 "
        "encoded key"
    )


#: The ``?key=value`` settings a ``truenas+*`` URI carries: the options that are
#: not secrets, spelled as hostctl's configs spell theirs. ``executor`` and
#: ``path`` repeat, in preference order; one empty value is "none".
_QUERY_KEYS = (
    "verify",
    "version",
    "executor",
    "path",
    "autologin",
    "timeout",
    "timeout_connect",
    "timeout_read",
    "timeout_write",
)

#: The `Timeout` field behind each ``timeout*`` key, as hostctl names them.
_TIMEOUT_KEYS = {
    "total": "timeout",
    "connect": "timeout_connect",
    "read": "timeout_read",
    "write": "timeout_write",
}

_TRUE_WORDS = frozenset(("1", "true", "yes", "on"))
_FALSE_WORDS = frozenset(("0", "false", "no", "off"))


def _query_bool(name: str, text: str) -> bool:
    word = text.casefold()
    if word in _TRUE_WORDS:
        return True
    if word in _FALSE_WORDS:
        return False
    raise ValueError(f"{name} must be one of 1/true/yes/on or 0/false/no/off")


def _query_options(parsed) -> "dict[str, object]":
    """The options a URI's query spells, as `TrueNASConfig` keywords.

    Strict: an unknown or repeated key is a ``ValueError`` (hostctl's
    :func:`~hostctl.uri.strict_uri_query`), so a misspelt ``?verfiy=0`` is
    refused instead of verifying anyway. ``verify`` is a boolean word or a CA
    bundle path; a ``timeout*`` value is seconds, empty for no limit.
    """
    query = _strict_uri_query(parsed, _QUERY_KEYS, repeatable=("executor", "path"))
    options: "dict[str, object]" = {}
    if "verify" in query:
        text = _ty.cast(str, query["verify"])
        word = text.casefold()
        if not text:
            raise ValueError("verify must be a boolean word or a CA bundle path")
        options["verify"] = (
            word in _TRUE_WORDS if word in _TRUE_WORDS | _FALSE_WORDS else text
        )
    if "version" in query:
        options["version"] = query["version"]
    for name in ("executor", "path"):
        if name in query:
            names = _ty.cast("tuple[str, ...]", query[name])
            options[name] = () if names == ("",) else names
    if "autologin" in query:
        options["autologin"] = _query_bool(
            "autologin", _ty.cast(str, query["autologin"])
        )
    fields: "dict[str, object]" = {}
    for field, key in _TIMEOUT_KEYS.items():
        if key not in query:
            continue
        text = _ty.cast(str, query[key])
        try:
            fields[field] = None if text == "" else float(text)
        except ValueError:
            raise ValueError(f"{key} must be a number of seconds") from None
    if fields:
        total = fields.pop("total", _DEFAULT)
        options["timeout"] = Timeout(
            _ty.cast(_ty.Any, total), **_ty.cast(_ty.Any, fields)
        )
    return options


def _seconds_text(value: object) -> str:
    """``20`` for 20.0, so a URI keeps a whole-second spelling."""
    number = float(_ty.cast(float, value))
    return str(int(number)) if number.is_integer() else repr(number)


def _shared_options(credentials: "_ty.Mapping[str, object]") -> "dict[str, object]":
    """Config options common to every branch of ``_from_parsed_uri``.

    Shared deliberately: that method returns from two places (the unix-socket
    form and the host/port form), and an option forwarded in only one would be
    accepted and silently ignored for the other.
    """
    return {
        "verify": _ty.cast(_ty.Any, credentials.get("verify", True)),
        "version": _ty.cast(str, credentials.get("version", "current")),
        "ssh": credentials.get("ssh"),
        "shell": _ty.cast(_ty.Any, credentials.get("shell")),
        "known_hosts": credentials.get("known_hosts", ()),
        "executor": _ty.cast(_ty.Any, credentials.get("executor")),
        "path": _ty.cast(_ty.Any, credentials.get("path")),
        "autologin": _ty.cast(bool, credentials.get("autologin", True)),
        "timeout": _ty.cast(_ty.Any, credentials.get("timeout", Timeout())),
    }


class _TrustAdapter(_req.adapters.HTTPAdapter):
    """HTTPS verified against exactly the context the websocket legs use.

    ``requests`` otherwise verifies against its own certifi bundle, so the side
    channels could trust what the API websocket does not -- see
    :mod:`pytruenas._tls`, which makes the one trust decision. A proxied
    request (``HTTPS_PROXY``) gets the same context through
    :meth:`proxy_manager_for`, as it does in hostctl's own adapter.
    """

    def __init__(self, context: "_ty.Any") -> None:
        self._context = context
        super().__init__()

    def init_poolmanager(self, *args, **kwargs):
        kwargs["ssl_context"] = self._context
        return super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, proxy, **proxy_kwargs):
        proxy_kwargs["ssl_context"] = self._context
        return super().proxy_manager_for(proxy, **proxy_kwargs)

    def cert_verify(self, conn, url, verify, cert):
        super().cert_verify(conn, url, bool(verify), cert)
        # requests points a verifying connection at a CA bundle file (certifi,
        # or its env vars); drop it so the context is the only trust source.
        conn.ca_certs = None
        conn.ca_cert_dir = None


def _ssh_config_from(
    shell: "_ty.Optional[str]", known_hosts: object = (), verify: bool = True
):
    """Build an :class:`hostctl.SSHConfig` from a shell connection string.

    Accepts what ``TrueNASClient(shell=...)`` has always taken --
    ``"ssh://root@nas"``, ``"root:pw@nas:22"``, a bare host -- so reaching the
    SSH leg does not require importing and assembling an SSHConfig by hand.
    ``None`` or a local target yields ``None``: no SSH leg.

    ``known_hosts`` and ``verify`` are hostctl's own fields, passed through:
    ``()`` checks the host key against the ssh_config's
    ``UserKnownHostsFile``, else ``~/.ssh/known_hosts``, unless
    ``verify`` is false, and a path or list names the trusted keys, checked
    either way.

    The user's ``~/.ssh/config`` applies, as it does for ``ssh``: a user or
    port in ``shell`` wins over its ``User``/``Port``, and with no ``User``
    from either the login is ``root``, TrueNAS's administrative login.
    """
    if not shell:
        return None

    from hostctl import SSHConfig

    target = _TGT.parse(shell, resolve_port=False, scheme="ssh")
    if target.scheme == "local" or not target.host:
        return None

    username = target.username or None
    password = target.password or None
    client_keys = None
    # "client_keys|root" in the username names the auth type, with the key as
    # the password; it is unpacked into SSHConfig's own fields.
    if username and "|" in username:
        logintype, username = username.split("|", maxsplit=1)
        if logintype == "client_keys" and password:
            client_keys = [password.encode() if isinstance(password, str) else password]
            password = None
    return SSHConfig(
        host=target.host,
        port=target.port or None,
        username=username or None,
        password=password,
        client_keys=client_keys,
        executable=target.path or None,
        verify=verify,
        known_hosts=_ty.cast(_ty.Any, known_hosts),
        default_username="root",
    )


def _timeout(value: object) -> Timeout:
    """``value`` as the `Timeout` a `TrueNASConfig` keeps, or ``ValueError``.

    A number or ``None`` is ``total``, as hostctl's configs take it. ``write``
    has no meaning here, and neither has ``read=0`` (a call always waits for
    its answer).
    """
    timeout = Timeout.coerce(_ty.cast(_ty.Any, value))
    if timeout.write is not _DEFAULT:
        raise ValueError("TrueNASConfig: timeout.write is not supported")
    if timeout.read == 0:
        raise ValueError("TrueNASConfig: timeout.read=0 (do not wait) is not supported")
    return timeout


def _as_names(
    value: "_ty.Optional[_ty.Union[_ty.Iterable[str], str]]",
) -> "_ty.Optional[tuple[str, ...]]":
    """Normalize a provider override to a tuple of names, or ``None``.

    A bare string is a single name, not an iterable of characters -- ``"ssh"``
    must not become ``("s", "s", "h")``.
    """
    if value is None:
        return None
    if isinstance(value, str):
        return (value,)
    return tuple(str(item) for item in value)


def _normalize_target(target: "_ty.Optional[str]") -> str:
    """Rewrite any accepted connection string into a canonical ``truenas+*`` URI.

    This is the single place the non-``truenas`` spellings are understood, and
    it is deliberately pure: no DNS, no HTTP, no filesystem. Everything it does
    is decided from the string alone.

    A local target *without* a port resolves to the middleware unix socket,
    matching today's behavior; a local target *with* a port does not, because an
    explicit port means the caller wants a real websocket (see
    ``client.py``'s ``is_local and not port`` guards).
    """
    if target is None:
        target = ""
    target = target.strip()

    if not target:
        return f"{_SCHEME_PREFIX}unix://{DEFAULT_SOCKET_PATH}"
    if target.startswith("/"):
        # A filesystem path has no host to reach: it is a unix socket.
        return f"{_SCHEME_PREFIX}unix://{_quote(target, safe=_SOCKET_PATH_SAFE)}"

    # A bare host or "host:port" has no scheme. Detecting that by "://" rather
    # than urlsplit's parsing avoids "nas:8080" being read as scheme "nas".
    if "://" not in target:
        scheme = ""
        remainder = target
    else:
        scheme, remainder = target.split("://", 1)
        scheme = scheme.lower()

    try:
        canonical = _SCHEME_ALIASES[scheme]
    except KeyError:
        raise ValueError(f"unsupported TrueNAS connection scheme: {scheme}") from None

    if canonical == f"{_SCHEME_PREFIX}unix":
        # ws+unix:///path -> the authority is empty and the path is the socket.
        path = remainder.lstrip("/")
        return (
            f"{_SCHEME_PREFIX}unix:///{path}"
            if path
            else (f"{_SCHEME_PREFIX}unix://{DEFAULT_SOCKET_PATH}")
        )

    # A URI that PARSES is taken at face value -- the same contract hostctl
    # states for `ConnectionString`/`redact_uri` (0.3.2). `wss://nas/x@y` is a
    # path containing an "@", not a credential, and no amount of guessing can
    # tell that from a password someone forgot to encode.
    #
    # What is refused is input that does not parse at all: an unencoded "/",
    # "?" or "#" in a password ends the authority early, so `user:secret` is
    # read as host:port and the port is not a number. Touching `.port` is what
    # detects it (it is a property that raises), and the message renders
    # through `redact`, whose own fallback handles exactly this shape.
    try:
        _urlsplit(f"{canonical}://{remainder}").port
    except ValueError:
        raise ValueError(
            "this connection string does not parse as a URI; percent-encode "
            "any '/', '?', '#', '@', '[' or ']' in the credentials (%2F, %3F, "
            "%23, %40, %5B, %5D): " + _redact_target(target)
        ) from None

    # Split the authority to spot the local-without-port case. Re-parse via
    # urlsplit on a normalized string so userinfo/IPv6 are handled properly.
    parsed = _urlsplit(f"{canonical}://{remainder}")
    host = (parsed.hostname or "").lower()
    is_local = host in _LOCAL_HOSTS and not parsed.path.strip("/")

    if is_local and not parsed.port:
        # Local with no port -> the middleware unix socket, as today.
        query = f"?{parsed.query}" if parsed.query else ""
        return f"{_SCHEME_PREFIX}unix://{DEFAULT_SOCKET_PATH}{query}"

    if is_local and scheme == "":
        # Local *with* an explicit port is a real websocket, and there is
        # nothing to probe: a loopback connection has no HTTPS redirect to
        # discover, so "auto" here would defer a decision that is already made.
        # Plain ws matches what client.py does for this case today.
        return f"{_SCHEME_PREFIX}ws://{remainder}"

    return f"{canonical}://{remainder}"


class TrueNASConfig(
    _HostConfig,
    schemes=(
        "truenas",
        "truenas+auto",
        "truenas+ws",
        "truenas+wss",
        "truenas+unix",
    ),
):
    """Parsed, credential-safe connection settings for a TrueNAS middleware host."""

    def __init__(
        self,
        host: str = "",
        *,
        port: int = 0,
        secure: "_ty.Optional[bool]" = None,
        socket_path: "_ty.Optional[str]" = None,
        api_path: "_ty.Optional[str]" = None,
        version: str = "current",
        verify: "_ty.Union[bool, str, _os.PathLike[str], _ssl.SSLContext]" = True,
        credentials: object = None,
        ssh: object = None,
        shell: "_ty.Optional[str]" = None,
        known_hosts: object = (),
        executor: "_ty.Optional[_ty.Union[_ty.Iterable[str], str]]" = None,
        path: "_ty.Optional[_ty.Union[_ty.Iterable[str], str]]" = None,
        autologin: bool = True,
        timeout: "_ty.Union[float, None, Timeout]" = Timeout(),
    ) -> None:
        super().__init__()
        #: A label assigned to `name`, replacing the derived one.
        self._name: "_ty.Optional[str]" = None
        #: Whether the first websocket access logs in automatically.
        self.autologin = autologin
        #: hostctl's `Timeout`: `connect` opens the websocket, `read` bounds one
        #: middleware call (and a side-channel read), `total` is `run()`'s
        #: default. `write` is not supported. See :attr:`timeouts`.
        self.timeout = _timeout(timeout)
        #: Explicit provider selection, overriding the defaults. Each is a name
        #: or a sequence of names, in preference order; ``None`` means "decide
        #: from the target". See :meth:`TrueNASClient.default_providers`.
        #:
        #: This replaced a ``webshell: bool`` flag, which was only ever the one
        #: hardcoded case of it (``executor=["ssh"]`` says the same thing, and
        #: says it in a form that also covers "SSH only", "force the web
        #: shell", or any other combination).
        self.executors = _as_names(executor)
        self.paths = _as_names(path)
        if not (host or port or socket_path or api_path) and secure is None:
            # Nothing names a remote host, so this is the local middleware.
            socket_path = DEFAULT_SOCKET_PATH
        self.host = host
        self.port = int(port or 0)
        #: ``True`` -> wss, ``False`` -> ws, ``None`` -> not given, use wss.
        self.secure = secure
        self.socket_path = socket_path
        self.api_path = api_path
        self.version = version
        #: One switch for every check the client makes. ``False`` turns off TLS
        #: certificate verification (the API websocket, the HTTP side channels,
        #: the web shell) and SSH host-key verification (commands and SFTP).
        #: ``True`` trusts the operating system; a CA bundle path (file or hashed
        #: directory) is trusted instead of it; an ``ssl.SSLContext`` is used as
        #: it is (client certificates, pinning). For SSH, a path or a context
        #: means "verify". With ``True``, ``$SSL_CERT_FILE`` and the other
        #: CA-bundle variables are consulted first; certifi is never used.
        self.verify: "_ty.Union[bool, str, _ssl.SSLContext]" = _tls.check(verify)
        #: The SSH leg. Accepts a ready :class:`hostctl.SSHConfig` or, via
        #: ``shell=``, the connection string ``TrueNASClient`` has always taken
        #: (``"ssh://root@nas"``, ``"root@nas:22"``) -- so a caller does not
        #: have to import and assemble an SSHConfig for the common case.
        #:
        #: ``known_hosts`` names the trusted host keys for an SSH leg built
        #: here -- from ``shell=`` or by :meth:`TrueNASClient.install_sshcreds`
        #: -- with hostctl's values: ``()`` is the ssh_config's
        #: ``UserKnownHostsFile``, else ``~/.ssh/known_hosts``; a path or list
        #: names the file(s). ``verify=False`` skips the ``()`` lookup;
        #: named keys are checked either way. An explicit ``ssh=SSHConfig(...)``
        #: keeps its ``known_hosts`` and gets ``verify=False`` on a copy.
        self.known_hosts = known_hosts
        if ssh is not None and verify is False and getattr(ssh, "verify", False):
            ssh = _dataclasses.replace(_ty.cast(_ty.Any, ssh), verify=False)
        self.ssh = (
            ssh
            if ssh is not None
            else _ssh_config_from(shell, known_hosts, verify is not False)
        )
        # Credentials are normalized once, here, so every downstream consumer
        # sees a Credentials instance rather than "maybe a string, maybe a
        # tuple, maybe None".
        self.credentials = (
            credentials
            if isinstance(credentials, _auth.Credentials)
            else _auth.Credentials(credentials)
        )

    # -- construction ------------------------------------------------------

    @classmethod
    def from_target(
        cls, target: "_ty.Optional[str]" = None, **options: object
    ) -> "TrueNASConfig":
        """Build a config from any connection string ``TrueNASClient`` accepts.

        This is pytruenas' entry point: it normalizes the string first (so bare
        ``wss://`` and friends work) and then hands it to hostctl's registry,
        which strips and parses any credentials in the userinfo.
        """
        uri = _normalize_target(target)
        config = _HostConfig(uri, **options)
        if not isinstance(config, cls):  # pragma: no cover - registry misconfig
            raise TypeError(f"{uri!r} did not resolve to a {cls.__name__}")
        return config

    #: Credential names accepted from ``HostConfig(uri, **credentials)``.
    #: hostctl checks this *before* construction, so a typo (``passwrd=``)
    #: raises instead of silently yielding a config with no password.
    uri_credentials = (
        # hostctl applies `username=`/`password=` over the URI's own user and
        # password before `_from_parsed_uri` runs (`password=""`: none).
        "username",
        "password",
        "otp",
        "api_key",
        "token",
        "credentials",
        "verify",
        "ssh",
        "version",
        "shell",
        "known_hosts",
        "executor",
        "path",
        "autologin",
        "timeout",
    )

    @classmethod
    def _from_parsed_uri(cls, parsed, **credentials: object) -> "TrueNASConfig":
        # `credentials` arrives already split by hostctl's parse_credentials --
        # a URI password's trailing "otp:123456" line is a separate key here, so
        # pytruenas does no string parsing of its own on this path. Unknown
        # names were already rejected against `uri_credentials` above.
        explicit = credentials.get("credentials")
        password = _ty.cast("str | None", credentials.get("password"))
        username = _unquote(parsed.username or "") or None
        given = _query_options(parsed)
        both = sorted(name for name in given if name in credentials)
        if both:
            raise ValueError(
                f"{both[0]} given both in the connection URI's query and as an "
                "argument"
            )
        credentials = {**credentials, **given}

        if explicit is not None and (
            password or credentials.get("api_key") or credentials.get("token")
        ):
            raise ValueError(
                "credentials given both in the connection URI and as an argument"
            )

        if explicit is not None:
            creds: object = explicit
        elif password or credentials.get("api_key") or credentials.get("token"):
            creds = _auth.Credentials.from_host_credentials(
                username=username,
                password=password,
                otp=_ty.cast("str | None", credentials.get("otp")),
                api_key=_ty.cast("str | None", credentials.get("api_key")),
                token=_ty.cast("str | None", credentials.get("token")),
            )
        else:
            creds = None

        scheme = parsed.scheme.casefold()
        if scheme == "truenas+unix":
            # "truenas+unix:///var/run/x.sock" puts the whole path in .path;
            # "truenas+unix://var/run/x.sock" puts its first segment in the
            # authority, so the two are joined. Unquoted: `a%3Fb` names `a?b`.
            first = parsed.netloc.rpartition("@")[2]
            socket_path = _unquote(f"/{first}{parsed.path}" if first else parsed.path)
            return cls(
                socket_path=socket_path.rstrip("/") or DEFAULT_SOCKET_PATH,
                credentials=creds,
                **_shared_options(credentials),
            )

        secure = None
        if scheme == "truenas+ws":
            secure = False
        elif scheme == "truenas+wss":
            secure = True

        # Named `uri_path`, not `path`: `path` is now a constructor keyword
        # (the path-provider override), and shadowing it here would be a
        # confusing near-miss for anyone editing this call.
        uri_path = parsed.path or ""
        return cls(
            # `uri_hostname`, not `parsed.hostname`: urlsplit case-folds the
            # host unconditionally (right for resolution, since DNS is
            # case-insensitive), but this value is rendered back out through
            # `connection_uri` and `name`, where echoing a spelling the
            # operator never typed turns a `nasA` fan-out into `[nasa]` logs.
            host=_uri_hostname(parsed),
            port=parsed.port or 0,
            secure=secure,
            api_path=uri_path if uri_path.strip("/") else None,
            credentials=creds,
            **_shared_options(credentials),
        )

    # -- derived state -----------------------------------------------------

    @property
    def timeouts(self) -> Timeout:
        """:attr:`timeout` with each ``DEFAULT`` replaced by what applies.

        ``connect`` is :data:`~pytruenas.connection.CONNECT_TIMEOUT`; ``read``
        is ``$PYTRUENAS_CALL_TIMEOUT`` when set, else
        :data:`~pytruenas.connection.CALL_TIMEOUT` (read now, not at import);
        ``total`` stays ``DEFAULT``: the command transport that runs a command
        applies its own.
        """
        given = self.timeout
        return Timeout(
            given.total,
            connect=(
                _connection.CONNECT_TIMEOUT
                if given.connect is _DEFAULT
                else given.connect
            ),
            read=(
                _connection.default_call_timeout()
                if given.read is _DEFAULT
                else given.read
            ),
        )

    @property
    def is_local(self) -> bool:
        """Whether this target is the local middleware unix socket."""
        return self.socket_path is not None

    @property
    def needs_scheme_probe(self) -> bool:
        """Whether the target left ws-vs-wss unsaid (so TLS is assumed).

        Not a pending action: this package never asks the server. It answers
        "was this decided by the caller or defaulted", which is what a caller
        that wants to probe for itself needs to know.
        """
        return not self.is_local and self.secure is None

    @property
    def needs_path_probe(self) -> bool:
        """Whether the target left the API path unsaid (so ``version`` is used).

        As with :attr:`needs_scheme_probe`, nothing here queries the server.
        """
        return not self.is_local and self.api_path is None

    @property
    def name(self) -> str:
        """A short label for this target: the hostname, not a whole URI.

        This is what belongs in a log prefix or a progress line. The scheme,
        port, API path and userinfo that :attr:`connection_uri` carries are
        noise once every record on the line repeats them -- and on a fan-out
        across ten hosts, the one thing a reader needs is *which machine*.

        ``localhost`` for the local middleware socket; the bare hostname
        otherwise, with the port appended only when it is non-default (a
        ``:8443`` is a real distinguisher between two entries for one host,
        where ``:443`` just repeats the scheme). Assigning it replaces the
        label.
        """
        if self._name is not None:
            return self._name
        if self.is_local:
            return "localhost"
        host = _uri_host(self.host) if self.host else "localhost"
        default_port = 443 if self.secure else 80
        if self.port and self.port != default_port:
            return f"{host}:{self.port}"
        return host

    @name.setter
    def name(self, value: str) -> None:
        self._name = str(value)

    @property
    def connection_uri(self) -> str:
        """The canonical, credential-free URI for this configuration.

        Every option that is not a secret and not at its default is in the
        query (``verify``, ``version``, ``executor``, ``path``, ``autologin``,
        ``timeout*``), so ``TrueNASConfig.from_target(config.connection_uri)``
        is an equal config. Credentials, the SSH leg and an
        ``ssl.SSLContext`` given as ``verify`` are not rendered.
        """
        query = _urlencode(self._query_pairs())
        query = f"?{query}" if query else ""
        if self.is_local:
            socket_path = _quote(self.socket_path or "", safe=_SOCKET_PATH_SAFE)
            return f"{_SCHEME_PREFIX}unix://{socket_path}{query}"
        if self.secure is None:
            scheme = AUTO_SCHEME
        else:
            scheme = f"{_SCHEME_PREFIX}wss" if self.secure else f"{_SCHEME_PREFIX}ws"
        authority = _uri_host(self.host)
        if self.port:
            authority = f"{authority}:{self.port}"
        return f"{scheme}://{authority}{self.api_path or ''}{query}"

    def _query_pairs(self) -> "list[tuple[str, str]]":
        """The non-default options as URI query pairs, in a fixed order."""
        pairs: "list[tuple[str, str]]" = []
        if self.verify is False:
            pairs.append(("verify", "false"))
        elif isinstance(self.verify, str):
            pairs.append(("verify", self.verify))
        if self.version != "current":
            pairs.append(("version", self.version))
        for key, names in (("executor", self.executors), ("path", self.paths)):
            if names is not None:
                pairs += [(key, name) for name in names] if names else [(key, "")]
        if not self.autologin:
            pairs.append(("autologin", "false"))
        for field, key in _TIMEOUT_KEYS.items():
            value = getattr(self.timeout, field)
            if value is not _DEFAULT:
                pairs.append((key, "" if value is None else _seconds_text(value)))
        return pairs

    def __eq__(self, other: object) -> bool:
        """Equal when :attr:`connection_uri` is: credentials are not compared."""
        if not isinstance(other, TrueNASConfig):
            return NotImplemented
        return self.connection_uri == other.connection_uri

    def __hash__(self) -> int:
        return hash(self.connection_uri)

    def __repr__(self) -> str:
        # Never render credentials: a config is logged, and connection_uri is
        # already the credential-free canonical form.
        return f"{type(self).__name__}({self.connection_uri!r})"

    def _create_host(self) -> "Host":
        return TrueNASClient(self)


#: Keywords `TrueNASClient(...)` routes to the config rather than to `PosixHost`:
#: exactly what `TrueNASConfig.from_target` accepts. `port=`, `secure=` and the
#: other constructor-only settings are spelled in the connection string.
_CONFIG_OPTIONS = frozenset(TrueNASConfig.uri_credentials)

#: Keywords that belong to `SystemHost` rather than the config (`info=`,
#: `initializer=`, ...). Derived from the signature too, so a hostctl release
#: that adds one does not turn it into a spurious "unknown argument" here.
_HOST_OPTIONS = frozenset(
    name
    for name, parameter in _inspect.signature(_PosixHost.__init__).parameters.items()
    if parameter.kind is _inspect.Parameter.KEYWORD_ONLY
)


def _ssh_pair(host: "TrueNASClient"):
    """The ``ssh`` and ``sftp`` providers: one resolver, so both share a transport.

    hostctl calls a resolver once per resolution however many names reach it;
    two calls would open two connections, only one of which is ever closed.
    """
    ssh = host._config.ssh
    if ssh is None:
        raise ValueError(
            "ssh/sftp providers were requested but no SSH configuration is set; "
            "pass ssh=SSHConfig(...) or call install_sshcreds()"
        )
    from hostctl import ssh_providers

    return ssh_providers(_ty.cast(_ty.Any, ssh))


def _webshell(host: "TrueNASClient"):
    from .webshell import WebShellExecutorProvider

    return WebShellExecutorProvider(_ty.cast(_ty.Any, host)), None


def _tnasws(host: "TrueNASClient"):
    from .providers import TrueNASWSPathProvider

    # The provider reaches the websocket lazily through the host, so building
    # it connects nothing.
    return None, TrueNASWSPathProvider(_ty.cast(_ty.Any, host))


class TrueNASClient(_PosixHost, _ty.Generic[ApiVersion]):
    """A TrueNAS middleware host: POSIX semantics over composed transports.

    Everything generic -- ``run``, ``path``, ``spawn``, ``info``, ``connect``,
    ``close``, ``shell``, ``capabilities``, ``last_selection`` -- is inherited
    from :class:`hostctl.host.PosixHost`, which selects between the providers
    assembled below. What this class adds is only the part no other host has:
    the middleware JSON-RPC websocket and the API surface built on it.

    Construct it from a connection string, a :class:`TrueNASConfig`, or nothing
    at all (the local middleware socket)::

        TrueNASClient("wss://nas")
        TrueNASClient("nas", credentials="1-...", executor=["ssh"])
        TrueNASClient(TrueNASConfig.from_target("wss://nas"))
        TrueNASClient()

    A string is normalized by :func:`_normalize_target`, and the keyword
    options are those of :meth:`TrueNASConfig.from_target`.

    Provider order depends on the target, and is overridable per selector with
    ``executor=``/``path=``:

    * **local** -- hostctl's stock ``local`` pair, and nothing else. Reaching
      this same machine over SSH, a PTY, or the filesystem API would be slower
      and strictly less capable.
    * **remote** -- ``ssh`` then ``webshell`` for commands, ``sftp`` then
      ``tnasws`` for paths. SSH leads on capability; the websocket legs follow
      through hostctl's selector, which records a redacted trace of what was
      tried (``host.last_selection``).
    """

    config_type = TrueNASConfig

    #: The descriptor names ``executor=``/``path=`` accept, beside hostctl's
    #: global ``local``. ``winrm`` is hidden: a TrueNAS host is POSIX.
    provider_resolvers = {
        "ssh": _ssh_pair,
        "sftp": _ssh_pair,
        "webshell": _webshell,
        "tnasws": _tnasws,
        "winrm": None,
    }

    # The overloads spell out the keywords `**options` routes, for an editor or
    # a type checker; `__init__` below is the one that runs.
    @_ty.overload
    def __init__(
        self,
        config: "_ty.Optional[str]" = None,
        *,
        credentials: object = ...,
        username: "_ty.Optional[str]" = ...,
        password: "_ty.Optional[str]" = ...,
        otp: "_ty.Optional[str]" = ...,
        api_key: "_ty.Optional[str]" = ...,
        token: "_ty.Optional[str]" = ...,
        verify: "_ty.Union[bool, str, _os.PathLike[str], _ssl.SSLContext]" = ...,
        ssh: "_ty.Optional[SSHConfig]" = ...,
        version: str = ...,
        shell: "_ty.Optional[str]" = ...,
        known_hosts: object = ...,
        executor: "_ty.Optional[_ty.Union[_ty.Iterable[str], str]]" = ...,
        path: "_ty.Optional[_ty.Union[_ty.Iterable[str], str]]" = ...,
        autologin: bool = ...,
        timeout: "_ty.Union[float, None, Timeout]" = ...,
        executor_providers: "_ty.Optional[_ty.Iterable[ExecutorProvider]]" = ...,
        path_providers: "_ty.Optional[_ty.Iterable[PathProvider]]" = ...,
        info: "_ty.Optional[HostInfo]" = ...,
        initializer: object = ...,
    ) -> None: ...

    @_ty.overload
    def __init__(
        self,
        config: TrueNASConfig,
        *,
        executor_providers: "_ty.Optional[_ty.Iterable[ExecutorProvider]]" = ...,
        path_providers: "_ty.Optional[_ty.Iterable[PathProvider]]" = ...,
        shell: object = ...,
        info: "_ty.Optional[HostInfo]" = ...,
        initializer: object = ...,
    ) -> None: ...

    def __init__(
        self,
        config: "_ty.Optional[_ty.Union[TrueNASConfig, str]]" = None,
        **options: object,
    ) -> None:
        # A connection string is the common case, so accept it directly rather
        # than making every caller reach for TrueNASConfig.from_target first.
        # hostctl's own `Host("uri")` shortcut cannot help here: its metaclass
        # only intercepts when `cls is Host`, so a subclass falls straight
        # through to normal construction.
        #
        # Keywords are split by destination: everything TrueNASConfig accepts
        # builds the config, and the rest (`info=`, `initializer=`, ...) goes
        # on to SystemHost. Splitting rather than guessing keeps a typo an
        # error from whichever layer owns the name.
        if config is None or isinstance(config, str):
            config_options = {
                key: options.pop(key) for key in list(options) if key in _CONFIG_OPTIONS
            }
            # Anything left that SystemHost does not take is a typo. Catch it
            # here rather than letting it reach SystemHost, which would raise a
            # TypeError naming an internal class -- unhelpful for a caller who
            # wrote `passwrd=` and needs to be told *that*.
            unknown = sorted(set(options) - _HOST_OPTIONS)
            if unknown:
                raise ValueError(
                    f"unknown credential argument: {unknown[0]!r} "
                    f"(configuration options: {', '.join(sorted(_CONFIG_OPTIONS))})"
                )
            config = TrueNASConfig.from_target(
                config, **_ty.cast(_ty.Any, config_options)
            )
        elif any(key in _CONFIG_OPTIONS for key in options):
            unexpected = ", ".join(
                sorted(key for key in options if key in _CONFIG_OPTIONS)
            )
            raise TypeError(
                "configuration options may not be combined with an existing "
                f"TrueNASConfig; pass them to from_target instead: {unexpected}"
            )
        self._config = config
        #: The live JSON-RPC connection, opened on first `.conn` access.
        self._conn: "_ty.Optional[_connection.TrueNASWSConnection]" = None
        # hostctl logs a provider fallback here too, once per skipped provider.
        _PosixHost.logger.fset(self, _resolve_logger(None, config.name))
        #: Guards opening, replacing and dropping `_conn`. Reentrant: logging
        #: in calls `auth.*` through `api`, which reads `conn` again.
        self._conn_lock = _threading.RLock()
        #: How the session last authenticated -- `login()`'s arguments -- so a
        #: reconnect repeats *that* login, not whatever the config would do.
        self._last_login: "_ty.Optional[tuple[object, dict]]" = None
        #: Closes the websocket if this host is collected without close().
        self._conn_finalizer: "_ty.Optional[_weakref.finalize]" = None
        #: One warning per host about credentials over plaintext ws://.
        self._plaintext_warned = False
        #: One warning per host when TLS verification is off.
        self._unverified_warned = False
        #: HTTP(S) session for the side channels; see `_http`.
        self._http_session: "_ty.Optional[_req.Session]" = None
        #: `{service: {method: is a job}}`, read once per service; see `_is_job`.
        self._job_flags: "dict[str, dict[str, bool]]" = {}

        super().__init__(config, **_ty.cast(_ty.Any, options))

    def default_providers(self):
        """The provider names for this target when ``executor=``/``path=`` name none.

        A local target is served entirely by hostctl's stock local pair: plain
        subprocess and plain local paths. Reaching this same machine through
        SSH, a PTY, or the filesystem API would be slower and strictly less
        capable, so no remote provider is offered.

        Remotely, SSH leads on capability (separate streams, real stdin, a rich
        POSIX path surface) and the websocket legs follow: the web shell as a
        command channel for a host with no reachable SSH, and ``tnasws`` for
        paths. hostctl drops a default ``ssh``/``sftp`` when its ``ssh`` extra
        is missing; a name the caller gives is kept and fails at use.
        """
        config = self._config
        if config.is_local:
            return ("local",), ("local",)
        if config.ssh is not None:
            return ("ssh", "webshell"), ("sftp", "tnasws")
        return ("webshell",), ("tnasws",)

    @property
    def logger(self) -> "_ty.Union[_logging.Logger, _logging.LoggerAdapter]":
        """The host's logger: every record it emits starts with ``[name]``.

        Assign a logger name or a ``Logger`` to send the records elsewhere;
        it is bound to :attr:`name` the same way. A ``LoggerAdapter`` is used
        as it is. The JSON-RPC connection takes the logger set when it opens.
        """
        return _PosixHost.logger.fget(self)  # type: ignore[attr-defined]

    @logger.setter
    def logger(
        self, value: "_ty.Union[str, _logging.Logger, _logging.LoggerAdapter, None]"
    ) -> None:
        _PosixHost.logger.fset(  # type: ignore[attr-defined]
            self, _resolve_logger(value, self.name)
        )

    # -- the TrueNAS surface ----------------------------------------------

    @property
    def _target(self):
        """The resolved websocket target as a :class:`~pytruenas.target.Target`.

        Built from the config rather than stored, so a change that resolves the
        scheme or API path later is picked up without re-syncing two copies.
        """
        config = self._config
        if config.is_local:
            # Built field by field: `Target.parse` would unquote the path, and a
            # `?` or `#` in the socket path would end it.
            socket_path = config.socket_path or DEFAULT_SOCKET_PATH
            return _TGT("ws+unix", "", "", "", 0, socket_path, "", "")
        scheme = "ws" if config.secure is False else "wss"
        authority = config.host
        if ":" in authority and not authority.startswith("["):
            # An IPv6 literal: without brackets its colons read as a port.
            authority = f"[{authority}]"
        if config.port:
            authority = f"{authority}:{config.port}"
        api_path = config.api_path or f"/api/{config.version}"
        return _TGT.parse(f"{scheme}://{authority}{api_path}", scheme=scheme)

    # -- middleware connection ---------------------------------------------

    def _openwss(self):
        config = self._config
        self._warn_if_unverified()
        # A unix socket is addressed by its path as given, not re-parsed as a
        # URI: `None` here meant "the default socket", so a configured
        # `socket_path` was silently ignored.
        uri = (
            _connection._UNIX_PREFIX + (config.socket_path or DEFAULT_SOCKET_PATH)
            if config.is_local
            else self._target.uri
        )
        timeouts = config.timeouts
        return _connection.TrueNASWSConnection(
            uri,
            verify=config.verify,
            call_timeout=_ty.cast("_ty.Optional[float]", timeouts.read),
            connect_timeout=_ty.cast("_ty.Optional[float]", timeouts.connect),
            # Share the host's name-bound logger, so a record from the
            # connection layer names the host it came from -- with several
            # clients open at once, an unattributed "connection was closed" is
            # not actionable.
            logger=self.logger,
        ).connect()

    @property
    def conn(self) -> "_connection.TrueNASWSConnection":
        """The live JSON-RPC connection; opens on first access.

        Logs in first when ``autologin`` is set (the default) and there is no
        live connection. Reconnects if the previous one closed; after a
        successful :meth:`login`, a reconnect repeats that login -- the same
        credentials and mechanism -- whatever ``autologin`` says.

        Thread-safe: concurrent first use opens one connection, not one per
        thread.
        """
        with self._conn_lock:
            conn = self._conn
            if conn is None or conn._closed.is_set():
                if self._last_login is not None:
                    creds, options = self._last_login
                    self.login(_ty.cast(_ty.Any, creds), **_ty.cast(_ty.Any, options))
                elif self._config.autologin:
                    self.login()
                else:
                    self._track(self._openwss())
                conn = self._conn
            return _ty.cast("_connection.TrueNASWSConnection", conn)

    def _track(self, conn: "_connection.TrueNASWSConnection") -> None:
        """Adopt ``conn`` as this host's connection, closing it on collection.

        A client dropped without ``close()`` (or its ``with`` block) left the
        websocket open and its reader thread alive for the life of the process.
        The finalizer holds the CONNECTION, never the host, so it does not keep
        the host alive; :meth:`close` detaches it.
        """
        self._conn = conn
        finalizer, self._conn_finalizer = self._conn_finalizer, None
        if finalizer is not None:
            finalizer.detach()
        self._conn_finalizer = _weakref.finalize(self, _close_quietly, conn)

    def connect(self) -> None:
        """Open the JSON-RPC connection, logging in when ``autologin`` is set.

        This is what ``with TrueNASClient(...)`` does on entry. The command and
        path transports (SSH, the web shell, SFTP) connect when first used, so
        an API-only script opens no shell session and dials no SSH port.
        Raises what opening :attr:`conn` raises.
        """
        self.conn

    def _drop_conn(self, conn: "_ty.Optional[_connection.TrueNASWSConnection]") -> None:
        """Discard ``conn`` so the next :attr:`conn` access reconnects.

        Only if it is still the current connection -- another thread may have
        replaced it already -- and closed, not just forgotten: a dropped
        reference would leak its socket and reader thread.
        """
        with self._conn_lock:
            if conn is not None and self._conn is conn:
                self._conn = None
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass

    def login(
        self,
        creds: "_ty.Optional[_auth.Credentials]" = None,
        *,
        login_ex: bool = False,
        login_options: "_ty.Optional[dict]" = None,
        otp_provider: "_ty.Optional[_ty.Callable[[], str]]" = None,
    ):
        """Open a fresh connection and authenticate.

        By default uses the legacy ``auth.login``/``login_with_*`` path. Pass
        ``login_ex=True`` for the modern mechanism, which supports 2FA via an
        ``OTP_REQUIRED`` continuation: the OTP comes from the credential's own
        ``otp`` if set, else from ``otp_provider()``. A credential with no
        login_ex form (e.g. local-socket auth) falls back automatically.

        Refused credentials raise :class:`~pytruenas.auth.AuthenticationError`
        on both paths, and the connection is closed rather than left open and
        unauthenticated. After a success, a reconnect repeats this login
        without the credential's one-time code, which is spent: on the
        ``login_ex`` path it asks ``otp_provider`` for a new one, and raises
        ``AuthenticationError("OTP_REQUIRED")`` without one.
        """
        options = {
            "login_ex": login_ex,
            "login_options": login_options,
            "otp_provider": otp_provider,
        }
        with self._conn_lock:
            if self._conn and not self._conn._closed.is_set():
                try:
                    self._conn.close()
                except Exception:
                    pass
            self._track(self._openwss())
            creds = creds or _ty.cast(_auth.Credentials, self._config.credentials)
            self._warn_if_plaintext(creds)
            try:
                if login_ex:
                    result = creds.login_ex(
                        _ty.cast(_ty.Any, self),
                        login_options=login_options,
                        otp_provider=otp_provider,
                    )
                else:
                    result = creds.login(_ty.cast(_ty.Any, self))
            except BaseException:
                conn, self._conn = self._conn, None
                conn.close()
                raise
            self._last_login = (_without_otp(creds), options)
            return result

    @_cached_property
    def api(self) -> "ApiVersion":
        """The root API namespace (``host.api.<namespace>.<method>(...)``).

        Parameterise the client to type it: ``TrueNASClient[Current]("nas").api``
        completes the generated API stubs.
        """
        return _ty.cast("ApiVersion", _Namespace(_ty.cast(_ty.Any, self)))

    @property
    def ssh(self):
        """The ``asyncssh`` connection ``run()`` uses (requires the ``ssh`` extra).

        For the rare caller that needs the raw connection -- port forwarding,
        an SFTP client of its own. Ordinary command and path work should go
        through :meth:`run` and :meth:`path`, which pick a transport rather
        than assuming this one exists.

        It is :attr:`hostctl.transports.ssh.SSHExecutorProvider.connection`:
        the first access connects (raising ``PermissionError``,
        ``ConnectionError``, ``TimeoutError`` or ``OSError``), and the
        connection is bound to that provider's ``loop``, hostctl's
        process-wide event-loop thread -- run its coroutines with
        ``asyncio.run_coroutine_threadsafe(coro, provider.loop).result()``.
        :meth:`close` closes it. Raises ``RuntimeError`` when this host has no
        SSH executor.
        """
        from hostctl.transports.ssh import SSHExecutorProvider

        for provider in self.executor_providers:
            if isinstance(provider, SSHExecutorProvider):
                return provider.connection
        raise RuntimeError(
            "no SSH transport is configured for this host; pass shell=... or "
            "ssh=SSHConfig(...), or call install_sshcreds()"
        )

    # -- convenience wrappers over common auth/core methods ----------------

    def me(self) -> dict:
        """The current session's authenticated user (``auth.me``)."""
        return _ty.cast(dict, self.api.auth.me())

    def logout(self) -> None:
        """End the current session (``auth.logout``)."""
        self.api.auth.logout()

    def ping(self) -> str:
        """Round-trip the middleware (``core.ping`` -> ``"pong"``)."""
        return _ty.cast(str, self.api.core.ping())

    # -- HTTP side channels ------------------------------------------------

    def _http_target(self, path: str):
        """This host's HTTP(S) URL for ``path``.

        The websocket ``ws``/``wss`` scheme maps to ``http``/``https``; used by
        the upload/download side channels and the web shell.

        ``path`` may carry a query string, because the middleware hands back
        download links that already do (``/_download/12345?auth_token=abc``).
        It is split off here rather than at each call site: assigning the whole
        string to ``path=`` percent-encodes the ``?`` and ``=`` into the path,
        so the server sees a filename containing ``%3F`` and 404s. Splitting in
        the one place every HTTP side channel goes through means the next
        caller handed a link with a query cannot reintroduce it.

        A fragment is dropped deliberately: it is a client-side construct and
        is never sent to the server, so carrying it would only mislead.

        The target's port is kept: a ``wss://nas:8443`` API means
        ``https://nas:8443`` side channels, and the uploads, downloads, file
        reads and web shell -- with their auth tokens -- must not go to 443.
        On the NAS itself (the unix-socket target) the side channels
        go to middlewared's own HTTP listener, ``http://127.0.0.1:6000``: there
        is no hostname to use, and nginx on 80 only redirects to 443.
        """
        path, _, query = path.partition("?")
        if self._config.is_local:
            return _TGT("http", "", "", "127.0.0.1", 6000, path, query, "")
        api = self._target
        scheme = "https" if api.scheme == "wss" else "http"
        default = 443 if scheme == "https" else 80
        port = 0 if api.port == default else api.port
        return api._replace(scheme=scheme, path=path, query=query, port=port)

    def upload(
        self,
        file: "_ty.Union[str, bytes]",
        method: str,
        *params,
        token=None,
        wait=True,
    ):
        """Upload ``file`` via ``/_upload``, then call ``method(*params)`` with it."""
        target = self._http_target("/_upload")
        data = {"method": method, "params": params}
        if isinstance(file, str):
            file = file.encode()

        if not token:
            # See the web shell: the server defaults match_origin to True and
            # this token is used once, by one HTTP request from this machine.
            token = self.api.auth.generate_token(5, {}, True, True)

        # An upload the middleware refuses answers with an HTTP error and an
        # HTML/JSON body; without the status check that surfaced as a KeyError
        # or a JSON decode error, naming neither the status nor the reason.
        resp = self._side_request(
            "POST",
            target.uri,
            headers={"Authorization": f"Token {token}"},
            files={"data": _js.dumps(data).encode(), "file": file},
        )
        try:
            jobid = resp.json()["job_id"]
        except (ValueError, KeyError, TypeError):
            raise _connection.ClientException(
                f"upload to {target.uri} returned no job id "
                f"(HTTP {resp.status_code}): {resp.text[:200]}"
            ) from None
        if wait:
            self.wait(jobid, callback=wait if callable(wait) else None)
        return jobid

    def _is_job(self, method: str) -> bool:
        """Whether middleware ``method`` runs as a job, per its schema's flag.

        Read for the whole service with ``core.get_methods`` (cached on disk by
        :func:`pytruenas.apicache.service_methods`, and here for the life
        of this client). A service that cannot be read counts as having no
        jobs, with one WARNING: the caller can still pass ``job=True``.
        """
        service = method.rpartition(".")[0]
        flags = self._job_flags.get(service)
        if flags is None:
            from . import apicache as _apicache

            try:
                found = _apicache.service_methods(self, service)
            # Asked after a create or an update already ran: failing to read
            # the flag must not turn that success into an error.
            except Exception as exc:
                self.logger.warning(
                    "cannot read which %s methods are jobs (%s); none is waited "
                    "on unless job=True is passed",
                    service,
                    exc,
                )
                found = {}
            flags = self._job_flags[service] = {
                name: bool(entry.get("job")) if isinstance(entry, dict) else False
                for name, entry in found.items()
            }
        return flags.get(method, False)

    #: Job states after which a job never changes again.
    JOB_DONE = ("SUCCESS", "FAILED", "ABORTED")

    def job_updates(
        self,
        job_id: int,
        *,
        timeout: "_ty.Optional[float]" = None,
        poll: float = 0.25,
        max_poll: float = 2.0,
    ) -> "_ty.Iterator[dict]":
        """Yield job ``job_id``'s record each time its state or progress changes.

        The record is ``core.get_jobs``'s: ``state`` (``WAITING``/``RUNNING``,
        then one of :attr:`JOB_DONE`), ``progress`` (``percent``,
        ``description``), ``result``, ``error``... The first record is always
        yielded and the finished one is always the last, so a loop over this
        can drive a log line or a progress bar and then inspect the outcome::

            for job in client.job_updates(job_id):
                print(job["progress"]["percent"], job["progress"]["description"])

        Polls with a back-off from ``poll`` to ``max_poll`` seconds, reset
        whenever something changes. ``timeout=None`` waits indefinitely;
        otherwise :class:`~pytruenas.connection.CallTimeout` is raised (the job
        keeps running on the server). Failure is not raised here -- the final
        record says so; :meth:`wait` raises it.
        """
        import time as _time

        deadline = None if timeout is None else _time.monotonic() + timeout
        delay = poll
        last = None
        while True:
            found = self.api.core.get_jobs([["id", "=", job_id]])
            if not found:
                raise _connection.ClientException(f"no such job: {job_id}")
            job = found[0]
            seen = (job.get("state"), _js.dumps(job.get("progress"), default=str))
            if seen != last:
                last = seen
                delay = poll
                yield job
            if job.get("state") in self.JOB_DONE:
                return
            if deadline is not None and _time.monotonic() + delay > deadline:
                raise _connection.CallTimeout()
            _time.sleep(delay)
            delay = min(delay * 2, max_poll)

    def wait(
        self,
        job_id: int,
        *,
        callback: "_ty.Optional[_ty.Callable[[dict], object]]" = None,
        timeout: "_ty.Optional[float]" = None,
    ) -> object:
        """Block until middleware job ``job_id`` finishes; return its result.

        ``callback(job)`` is called with the job record every time its state or
        progress changes (see :meth:`job_updates`) -- enough for a log line or
        a progress bar. ``SUCCESS`` returns the job's ``result``;
        ``FAILED``/``ABORTED`` raise :class:`~pytruenas.connection.JobFailed`
        carrying the record.

        Not ``core.job_wait``: that method is itself a job, so calling it
        returns a NEW job id immediately instead of blocking (measured on
        26.0.0-BETA.1: 0.4 s) -- every "wait" built on it returned early.
        """
        job: dict = {}
        for job in self.job_updates(job_id, timeout=timeout):
            if callback is not None:
                callback(job)
        if job.get("state") != "SUCCESS":
            raise _connection.JobFailed(job)
        return job.get("result")

    def download(
        self,
        method: str,
        *args,
        filename: "_ty.Optional[str]" = None,
        buffered=False,
        wait=True,
    ):
        """Call ``method`` for a download link and fetch it over HTTP(S).

        With ``wait`` (the default) returns the content, once the job that
        produced it has finished: a failed job raises
        :class:`~pytruenas.connection.JobFailed` rather than returning what
        was sent before it failed. ``buffered=True`` waits before fetching;
        otherwise the job streams into the response and is checked after it.
        ``wait=False`` returns a :class:`PendingDownload` instead of the bytes:
        its ``job_id``, and ``fetch()`` when they are wanted.
        """
        jobid, link = self.api.core.download(
            method, args, filename or "download", buffered
        )
        pending = PendingDownload(self, jobid, self._http_target(link).uri, buffered)
        if wait:
            return pending.fetch(callback=wait if callable(wait) else None)
        return pending

    def _side_request(self, method: str, uri: str, **kwargs) -> "_req.Response":
        """One HTTP(S) side-channel request, checked, bounded and token-free.

        A failure raises what :func:`_side_channel_error` makes of it. The
        connect and read timeouts are the websocket's own
        (``config.timeouts``).
        """
        timeouts = self._config.timeouts
        try:
            resp = self._http.request(
                method,
                uri,
                verify=self._http_verify,
                timeout=(timeouts.connect, timeouts.read),
                **kwargs,
            )
            resp.raise_for_status()
        except _req.RequestException as exc:
            # `from None`: requests' own error names the URL, token included.
            raise _side_channel_error(exc) from None
        return resp

    def dump_api(
        self, *, cache: bool = True, refresh: bool = False, all_versions: bool = False
    ):
        """Return the middleware API definition (``middlewared --dump-api``).

        The current API version only, pruned on the target before the
        transfer; ``all_versions=True`` keeps every version the appliance
        serves (current first), which is about five times the bytes on 26.0.

        The dump is built and **compressed on the target**, then fetched over
        SFTP when this host has an SSH leg and in verified chunks otherwise.
        Its raw output cannot come back through ``run()``: the dump is
        24,103,000 bytes on 26.0, and the web shell's PTY loses the connection
        on that much output, on the very hosts (no SSH) that need it.

        ``cache=True`` (the default) reads and writes the per-host, per-version
        cache under ``$PYTRUENAS_CACHE``; building the dump costs about 75
        seconds, which is not a price to pay twice. ``refresh=True`` re-fetches
        and overwrites it. See :mod:`pytruenas.apicache`.
        """
        from . import apicache as _apicache

        if not cache:
            return _apicache.fetch(self, all_versions=all_versions)
        return _apicache.load(self, refresh=refresh, all_versions=all_versions)

    def install_sshcreds(
        self, name: "_ty.Optional[str]" = None, private_key: "_ty.Optional[str]" = None
    ):
        """Provision an SSH keypair and wire it into this host's SSH transport.

        Generates (or reuses) a ``SSH_KEY_PAIR`` keychain credential, installs
        the public half on root's ``authorized_keys``, and stores the private
        half on :attr:`TrueNASConfig.ssh` as a real
        :class:`hostctl.SSHConfig`, as its ``client_keys``; an ``ssh=`` the
        caller passed is copied, not changed.

        Adding an SSH transport changes what this host can do, so the providers
        are rebuilt: a host that had no executor at all (remote, no SSH) gains
        one, and paths gain the richer SFTP leg.

        Does **not** require the optional ``ssh`` extra: provisioning runs
        entirely over the middleware API and opens no SSH connection. The one
        exception is passing ``private_key=`` for a key the host does not
        already know, where the public half has to be derived locally (see
        :func:`_public_key`). *Using* the SSH transport this configures still
        needs the extra, as it always did.
        """
        name = name or "pytruenas"
        keypair = self.api.keychaincredential._get(type="SSH_KEY_PAIR", name=name)
        # The middleware hands back BOTH halves on the paths it generates or
        # stores, so the public key is usually already known -- see `_public_key`
        # for why that matters.
        pubkey: "_ty.Optional[str]" = None
        if not keypair and not private_key:
            generated = self.api.keychaincredential.generate_ssh_key_pair()
            private_key = generated["private_key"]
            pubkey = generated.get("public_key")
        elif not private_key:
            attributes = keypair["attributes"]
            private_key = attributes["private_key"]
            pubkey = attributes.get("public_key")

        pubkey = (pubkey or "").strip() or _public_key(_ty.cast(str, private_key))
        keypair = self.api.keychaincredential._upsert(
            ("name", "type"),
            type="SSH_KEY_PAIR",
            name=name,
            attributes={"private_key": private_key, "public_key": pubkey},
        )
        root = self.api.user._get(username="root")
        authorized = (root.get("sshpubkey") or "").splitlines()
        if pubkey not in authorized:
            authorized.append(pubkey)
            # `("username",)` -- a one-item SEQUENCE, not the bare string. A
            # bare `str` selector is read as a record *id* (see
            # `DBAction.execute`); the tuple says "match on this field name",
            # which is what selecting root by username means.
            self.api.user._upsert(
                ("username",), username="root", sshpubkey="\n".join(authorized)
            )

        private_key = _ty.cast(str, keypair["attributes"]["private_key"])

        from hostctl import SSHConfig

        # A local target has no host to SSH *to*, and needs none -- commands
        # already run here. The keypair is still provisioned (it is installed
        # on root's authorized_keys, so other machines can use it), but there
        # is no leg to wire it into.
        if self._config.is_local:
            return private_key

        existing = self._config.ssh
        if existing is None:
            self._config.ssh = SSHConfig(
                host=self._config.host,
                username="root",
                client_keys=[private_key.encode()],
                verify=self._config.verify is not False,
                known_hosts=_ty.cast(_ty.Any, self._config.known_hosts),
            )
        elif not existing.password and not existing.client_keys:
            # A copy: the caller's `ssh=` object may serve other hosts too.
            self._config.ssh = _dataclasses.replace(
                existing, client_keys=[private_key.encode()]
            )
        else:
            # Explicit credentials win: a caller who configured their own auth
            # is not silently overridden by a provisioning call.
            return private_key

        # One resolution and one swap: the ssh and sftp legs share a
        # transport, and hostctl closes each replaced one (an open SSH
        # connection among them) once.
        executors, paths = self.resolve_providers()
        self.replace_providers(executor=executors, path=paths)
        return private_key

    def _warn_if_unverified(self) -> None:
        """Warn once when TLS certificates go unchecked for a remote target."""
        config = self._config
        if config.verify is not False or config.is_local or config.secure is False:
            return
        if self._unverified_warned:
            return
        self._unverified_warned = True
        self.logger.warning(
            "TLS certificate verification is off for %s (verify=False)", config.name
        )

    def _warn_if_plaintext(self, creds: object) -> None:
        """Warn once when credentials would travel over plain ``ws://``.

        Not a refusal: ``ws://`` is documented and legitimate for a loopback
        target or a tunnel, and pytruenas cannot know which one this is. But a
        password or API key on a plaintext socket to another machine is worth a
        line in the log, since the usual cause is a target typed without its
        scheme somewhere that defaults to ws.
        """
        config = self._config
        if config.is_local or config.secure is not False:
            return
        host = (config.host or "").lower()
        if host in _LOCAL_HOSTS or host in ("::1", "[::1]"):
            return
        if creds is None or isinstance(creds, _auth.LocalAuth):
            return
        if self._plaintext_warned:
            return
        self._plaintext_warned = True
        self.logger.warning(
            "sending credentials over plaintext ws:// to %s; use wss:// (or a "
            "tunnel) unless this link is already private",
            config.name,
        )

    def path(self, *segments, backend=None):
        """A path on the target -- :meth:`hostctl.host.Host.path`, rooted at ``/``.

        On a remote target a relative path (and ``path()`` with no segments)
        names the same file on every leg: ``/`` joined with it. hostctl's SFTP
        leg reads a relative path against the SSH login directory, which the
        websocket leg cannot know, so left relative the same path would name
        different files depending on which leg serves it. A local target keeps
        local semantics (the process's working directory).

        ``backend`` pins the path to that provider for every operation on it.
        """
        if not self._config.is_local and (
            not segments or not str(segments[0]).startswith("/")
        ):
            segments = ("/", *segments)
        return super().path(*segments, backend=backend)

    @property
    def _http(self) -> "_req.Session":
        """The HTTP(S) session behind the side channels (upload, download).

        With verification on, HTTPS trusts exactly what the API websocket
        does (see :mod:`pytruenas._tls`).
        """
        if self._http_session is None:
            session = _req.Session()
            self._warn_if_unverified()
            context = _tls.context(self._config.verify)
            if context is not None:
                session.mount("https://", _TrustAdapter(context))
            self._http_session = session
        return self._http_session

    @property
    def _http_verify(self) -> bool:
        """``verify=`` for each side-channel request.

        Passed per request, never set on the session: ``requests`` replaces a
        request-level ``None`` with ``$REQUESTS_CA_BUNDLE`` *before* merging the
        session's ``verify=False``, so a session-level ``False`` verifies anyway
        whenever that variable is set (measured).
        """
        return self._config.verify is not False

    def close(self) -> None:
        """Close the transports, then the websocket.

        Order matters: the ``tnasws`` path provider talks over the websocket,
        so it must be torn down before the connection it depends on.
        """
        finalizer, self._conn_finalizer = self._conn_finalizer, None
        if finalizer is not None:
            # Closing explicitly; nothing left for the collector to do.
            finalizer.detach()
        session, self._http_session = self._http_session, None
        if session is not None:
            session.close()
        try:
            super().close()
        finally:
            conn, self._conn = self._conn, None
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    # close() must be safe to call repeatedly and must not mask
                    # an error raised by the provider teardown above.
                    pass


# `auth` and `namespace` name the client in their annotations, but this module
# imports them, so they cannot import it: bind it for `typing.get_type_hints`.
setattr(_auth, "TrueNASClient", TrueNASClient)
setattr(_namespace, "TrueNASClient", TrueNASClient)

__all__ = [
    "AUTO_SCHEME",
    "DEFAULT_SOCKET_PATH",
    "PendingDownload",
    "TrueNASClient",
    "TrueNASConfig",
]
