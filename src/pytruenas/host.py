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

import importlib.util as _importlib_util
import inspect as _inspect
import json as _js
import logging as _logging
import os as _os
import threading as _threading
import typing as _ty
import weakref as _weakref
from functools import cached_property as _cached_property
from urllib.parse import unquote as _unquote
from urllib.parse import urlsplit as _urlsplit

import requests as _req
from hostctl.host import HostConfig as _HostConfig
from hostctl.host import PosixHost as _PosixHost
from hostctl.host import uri_host as _uri_host
from hostctl.host import uri_hostname as _uri_hostname

from . import auth as _auth
from . import connection as _connection
from .connection import DEFAULT_UNIX_SOCKET
from .namespace import Namespace as _Namespace
from .fs._uri import quote_uri_path as _quote_uri_path
from .utils import tls as _tls
from .utils.target import Target as _TGT
from .utils.target import redact as _redact_target

if _ty.TYPE_CHECKING:  # pragma: no cover - typing only
    from hostctl.host import Host
    from truenasapi_typings.current import Current

    #: Mirrors `TrueNASClient`'s parameter so `TrueNASHost[Current]` gives the
    #: same completion on `.api` that `TrueNASClient[Current]` does.
    ApiVersion = _ty.TypeVar(
        "ApiVersion", bound=_Namespace, default=Current  # type: ignore
    )
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

#: Hosts that mean "this machine" -- matching ``Target.is_local`` so the
#: local-socket shortcut behaves exactly as it does today.
_LOCAL_HOSTS = {"", "localhost", "127.0.0.1"}

#: Provider names accepted by the ``executor=``/``path=`` overrides.
EXECUTOR_NAMES = ("local", "ssh", "webshell")
PATH_NAMES = ("local", "sftp", "tnasws")


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

    ``.trace`` is forwarded if the underlying logger has it (``duho.logging``
    installs a TRACE level); :mod:`pytruenas.namespace` calls it for per-call
    logging, and a plain ``logging.Logger`` has no such method.
    """

    def process(self, msg, kwargs):
        prefix = f"[{self.extra['name']}] " if self.extra else ""
        text = str(msg)
        if prefix and text.startswith(prefix):
            return text, kwargs
        return f"{prefix}{text}", kwargs

    def trace(self, msg, *args, **kwargs):
        # LoggerAdapter forwards only the standard levels; TRACE is duho's
        # addition, and namespace.py calls it on every API call.
        inner = getattr(self.logger, "trace", None)
        if inner is None:  # pragma: no cover - only without duho's logging setup
            return
        msg, kwargs = self.process(msg, kwargs)
        inner(msg, *args, **kwargs)


def _close_quietly(closeable: object) -> None:
    """Close something during garbage collection, where raising is useless."""
    close = getattr(closeable, "close", None)
    if not callable(close):
        return
    try:
        close()
    except Exception:  # pragma: no cover - interpreter teardown
        pass


def _close_provider(provider: object) -> None:
    """Close a provider's transport, if it has one that can be closed."""
    transport = getattr(provider, "transport", None)
    for candidate in (transport, provider):
        close = getattr(candidate, "close", None)
        if callable(close):
            try:
                close()
            except Exception:  # pragma: no cover - teardown must not raise
                _logging.getLogger("pytruenas").debug(
                    "closing %r failed", candidate, exc_info=True
                )
            return


def _resolve_logger(logger: object, name: "str | None" = None):
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
    except ImportError as exc:  # pragma: no cover - only without the extra
        raise ImportError(
            "SSH/SFTP support requires the 'ssh' extra: pip install pytruenas[ssh]"
        ) from exc
    return asyncssh


def _ssh_available() -> bool:
    """Whether an SSH/SFTP leg can actually be built (the ``ssh`` extra).

    Uses :func:`importlib.util.find_spec` rather than importing: this runs
    during provider construction, which happens for every client including ones
    that will never touch SSH, and importing asyncssh is not cheap.

    Deliberately answers "can it be imported", not "is it configured" -- those
    are different questions, and conflating them is what let a configured-but-
    uninstallable SSH leg reach the point of use before failing.
    """
    return _importlib_util.find_spec("asyncssh") is not None


def _public_key(private_key: str) -> str:
    """Derive the OpenSSH public key for ``private_key``.

    Only reached when the public half is genuinely unknown -- a caller who
    passed ``private_key=`` to :meth:`TrueNASHost.install_sshcreds` and nothing
    else. Every other path gets both halves from the middleware, which is what
    keeps ``install_sshcreds`` usable without the optional ``ssh`` extra: it
    provisions a keypair through the API and never opens an SSH connection, so
    requiring ``asyncssh`` for the common case was a dependency on a library
    that was not being used to do anything.

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


class _Default:
    """Sentinel: an option was not given, so it follows ``verify``."""

    def __repr__(self) -> str:
        return "<follows verify>"


#: ``known_hosts`` not given. Distinct from ``()`` (check the usual file) and
#: from ``None`` (do not check), both of which are real choices.
_DEFAULT: _ty.Any = _Default()


def _shared_options(credentials: "_ty.Mapping[str, object]") -> "dict[str, object]":
    """Config options common to every branch of ``_from_parsed_uri``.

    Shared deliberately: that method returns from two places (the unix-socket
    form and the host/port form), and an option forwarded in only one is
    silently ignored for the other. That is not hypothetical -- it is exactly
    how ``webshell=False`` was once accepted and dropped.
    """
    return {
        "verify": _ty.cast(bool, credentials.get("verify", True)),
        "sslverify": _ty.cast(_ty.Any, credentials.get("sslverify")),
        "version": _ty.cast(str, credentials.get("version", "current")),
        "ssh": credentials.get("ssh"),
        "shell": _ty.cast(_ty.Any, credentials.get("shell")),
        "known_hosts": credentials.get("known_hosts", _DEFAULT),
        "executor": _ty.cast(_ty.Any, credentials.get("executor")),
        "path": _ty.cast(_ty.Any, credentials.get("path")),
        "autologin": _ty.cast(bool, credentials.get("autologin", True)),
        "logger": credentials.get("logger"),
    }


class _TrustAdapter(_req.adapters.HTTPAdapter):
    """HTTPS verified against exactly the context the websocket legs use.

    ``requests`` otherwise verifies against its own certifi bundle, which is how
    the side channels once disagreed with the API websocket -- see
    :mod:`pytruenas.utils.tls`, which makes the one trust decision.
    """

    def __init__(self, context: "_ty.Any") -> None:
        self._context = context
        super().__init__()

    def init_poolmanager(self, *args, **kwargs):
        kwargs["ssl_context"] = self._context
        return super().init_poolmanager(*args, **kwargs)

    def cert_verify(self, conn, url, verify, cert):
        super().cert_verify(conn, url, bool(verify), cert)
        # requests points a verifying connection at a CA bundle file (certifi,
        # or its env vars); drop it so the context is the only trust source.
        conn.ca_certs = None
        conn.ca_cert_dir = None


def _ssh_config_from(shell: "str | None", known_hosts: object = ()):
    """Build an :class:`hostctl.host.SshConfig` from a shell connection string.

    Accepts what ``TrueNASClient(shell=...)`` has always taken --
    ``"ssh://root@nas"``, ``"root:pw@nas:22"``, a bare host -- so reaching the
    SSH leg does not require importing and assembling an SshConfig by hand.
    ``None`` or a local target yields ``None``: no SSH leg.

    ``known_hosts`` is hostctl's own field, passed through unchanged: ``()``
    (the default) checks the host key against the usual ``~/.ssh/known_hosts``,
    ``None`` does not check it, a path or list names the file(s) to use.
    """
    if not shell:
        return None

    from hostctl.host import SshConfig

    target = _TGT.parse(shell, scheme="ssh")
    if target.scheme == "local" or not target.host:
        return None

    username = target.username or "root"
    password = target.password or None
    client_keys = None
    # The pre-hostctl client packed the auth type into the username as
    # "client_keys|root"; accept it so an existing connection string keeps
    # working, but unpack it into SshConfig's real fields.
    if "|" in username:
        logintype, username = username.split("|", maxsplit=1)
        if logintype == "client_keys" and password:
            client_keys = [password.encode() if isinstance(password, str) else password]
            password = None
    return SshConfig(
        host=target.host,
        port=target.port or 22,
        username=username or "root",
        password=password,
        client_keys=client_keys,
        executable=target.path or None,
        known_hosts=_ty.cast(_ty.Any, known_hosts),
    )


def _reject_unknown(
    names: "_ty.Sequence[str]", allowed: "_ty.Sequence[str]", kind: str
) -> None:
    """Fail on an unrecognised provider name rather than silently ignoring it.

    A typo (``executor=["shh"]``) would otherwise compose a host with no
    executor at all and no complaint, surfacing much later as a confusing
    "no provider is available".
    """
    unknown = [name for name in names if name not in allowed]
    if unknown:
        raise ValueError(
            f"unknown {kind} provider: {unknown[0]!r} "
            f"(available: {', '.join(allowed)})"
        )


def _as_names(value: "_ty.Iterable[str] | str | None") -> "tuple[str, ...] | None":
    """Normalize a provider override to a tuple of names, or ``None``.

    A bare string is a single name, not an iterable of characters -- ``"ssh"``
    must not become ``("s", "s", "h")``.
    """
    if value is None:
        return None
    if isinstance(value, str):
        return (value,)
    return tuple(str(item) for item in value)


def _normalize_target(target: "str | None") -> str:
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
            "any '/', '?', '#' or '@' in the credentials (%2F, %3F, %23, "
            "%40): " + _redact_target(target)
        ) from None

    # Split the authority to spot the local-without-port case. Re-parse via
    # urlsplit on a normalized string so userinfo/IPv6 are handled properly.
    parsed = _urlsplit(f"{canonical}://{remainder}")
    host = (parsed.hostname or "").lower()
    is_local = host in _LOCAL_HOSTS and not parsed.path.strip("/")

    if is_local and not parsed.port:
        # Local with no port -> the middleware unix socket, as today.
        return f"{_SCHEME_PREFIX}unix://{DEFAULT_SOCKET_PATH}"

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
        secure: "bool | None" = None,
        socket_path: "str | None" = None,
        api_path: "str | None" = None,
        version: str = "current",
        verify: bool = True,
        sslverify: "bool | str | _os.PathLike[str] | None" = None,
        credentials: object = None,
        ssh: object = None,
        shell: "str | None" = None,
        known_hosts: object = _DEFAULT,
        executor: "_ty.Iterable[str] | str | None" = None,
        path: "_ty.Iterable[str] | str | None" = None,
        autologin: bool = True,
        logger: object = None,
    ) -> None:
        super().__init__()
        #: Whether the first websocket access logs in automatically.
        self.autologin = autologin
        #: Logger for the client built from this config; a name or a Logger.
        self.logger = logger
        #: Explicit provider selection, overriding the defaults. Each is a name
        #: or a sequence of names, in preference order; ``None`` means "decide
        #: from the target". See :meth:`TrueNASHost._build_providers`.
        #:
        #: This replaced a ``webshell: bool`` flag, which was only ever the one
        #: hardcoded case of it (``executor=["ssh"]`` says the same thing, and
        #: says it in a form that also covers "SSH only", "force the web
        #: shell", or any other combination).
        self.executors = _as_names(executor)
        self.paths = _as_names(path)
        self.host = host
        self.port = int(port or 0)
        #: ``True`` -> wss, ``False`` -> ws, ``None`` -> not given, use wss.
        self.secure = secure
        self.socket_path = socket_path
        self.api_path = api_path
        self.version = version
        #: One switch for every check the client makes: ``False`` turns off TLS
        #: certificate verification (the API websocket, the HTTP side channels,
        #: the web shell) and SSH host-key verification (commands and SFTP).
        #: ``sslverify=`` / ``known_hosts=`` given explicitly override it.
        self.verify = verify
        #: TLS certificate verification; follows ``verify`` unless given. A
        #: path is a CA bundle (file or hashed directory) trusted instead of
        #: the OS store; with ``True``, ``$SSL_CERT_FILE`` and the other
        #: :data:`~pytruenas.utils.tls.CA_BUNDLE_ENV` variables are consulted
        #: first. certifi is never used.
        if sslverify is None:
            sslverify = verify
        elif not isinstance(sslverify, bool):
            sslverify = _os.fspath(sslverify)
        self.sslverify: "bool | str" = sslverify
        #: The SSH leg. Accepts a ready :class:`hostctl.host.SshConfig` or, via
        #: ``shell=``, the connection string ``TrueNASClient`` has always taken
        #: (``"ssh://root@nas"``, ``"root@nas:22"``) -- so a caller does not
        #: have to import and assemble an SshConfig for the common case.
        #:
        #: ``known_hosts`` is the host-key policy for an SSH leg built here --
        #: from ``shell=`` or by :meth:`TrueNASHost.install_sshcreds`. It uses
        #: hostctl's values: ``()`` checks ``~/.ssh/known_hosts``, ``None``
        #: disables the check, a path or list names the file(s). Unset, it
        #: follows ``verify`` (``()`` or ``None``). An explicit
        #: ``ssh=SshConfig(...)`` keeps a policy it names; one left at the
        #: ``()`` default gets ``None`` when ``verify=False`` (on a copy).
        if known_hosts is _DEFAULT:
            known_hosts = () if verify else None
        self.known_hosts = known_hosts
        if ssh is not None and not verify and getattr(ssh, "known_hosts", None) == ():
            import dataclasses

            ssh = dataclasses.replace(_ty.cast(_ty.Any, ssh), known_hosts=None)
        self.ssh = ssh if ssh is not None else _ssh_config_from(shell, known_hosts)
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
        cls, target: "str | None" = None, **options: object
    ) -> "TrueNASConfig":
        """Build a config from any connection string ``TrueNASClient`` accepts.

        This is pytruenas' entry point: it normalizes the string first (so bare
        ``wss://`` and friends work) and then hands it to hostctl's registry,
        which strips and parses any credentials in the userinfo.
        """
        uri = _normalize_target(target)
        config = _HostConfig._from_uri(uri, **options)
        if not isinstance(config, cls):  # pragma: no cover - registry misconfig
            raise TypeError(f"{uri!r} did not resolve to a {cls.__name__}")
        return config

    #: Credential names accepted from ``HostConfig(uri, **credentials)``.
    #: hostctl checks this *before* construction, so a typo (``passwrd=``)
    #: raises instead of silently yielding a config with no password.
    uri_credentials = (
        "password",
        "otp",
        "api_key",
        "token",
        "credentials",
        "verify",
        "sslverify",
        "ssh",
        "version",
        "shell",
        "known_hosts",
        "executor",
        "path",
        "autologin",
        "logger",
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
            # urlsplit puts a leading "///path" entirely in .path; a
            # "truenas+unix://var/run/..." spelling lands in .netloc instead.
            #
            # Unquoted, as a URI path must be: `unix:///run/a%3Fb/x.sock` names
            # the file `/run/a?b/x.sock`, and connecting to the literal
            # `%3F` spelling would open a different one (or nothing). The
            # encoded form is how such a path is written in a URI at all --
            # raw, the `?` would end the path.
            socket_path = _unquote(parsed.path) or f"/{_unquote(parsed.netloc)}"
            return cls(
                socket_path=socket_path or DEFAULT_SOCKET_PATH,
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
        where ``:443`` just repeats the scheme).
        """
        if self.is_local:
            return "localhost"
        host = _uri_host(self.host) if self.host else "localhost"
        default_port = 443 if self.secure else 80
        if self.port and self.port != default_port:
            return f"{host}:{self.port}"
        return host

    @property
    def connection_uri(self) -> str:
        """The canonical, credential-free URI for this configuration."""
        if self.is_local:
            return f"{_SCHEME_PREFIX}unix://{self.socket_path}"
        if self.secure is None:
            scheme = AUTO_SCHEME
        else:
            scheme = f"{_SCHEME_PREFIX}wss" if self.secure else f"{_SCHEME_PREFIX}ws"
        authority = _uri_host(self.host)
        if self.port:
            authority = f"{authority}:{self.port}"
        return f"{scheme}://{authority}{self.api_path or ''}"

    def __repr__(self) -> str:
        # Never render credentials: a config is logged, and connection_uri is
        # already the credential-free canonical form.
        return f"{type(self).__name__}({self.connection_uri!r})"

    def _create_host(self) -> "Host":
        return TrueNASHost(self)


#: Keywords `TrueNASHost(...)` should route to the config rather than to
#: `SystemHost`. Derived from the signature so the two cannot drift: adding a
#: `TrueNASConfig` parameter makes it accepted here automatically.
#: `signature(TrueNASConfig)` would resolve through HostConfig's metaclass
#: `__call__`, not the constructor, so read `__init__` directly.
_CONFIG_OPTIONS = frozenset(
    name
    for name, parameter in _inspect.signature(TrueNASConfig.__init__).parameters.items()
    if parameter.kind is _inspect.Parameter.KEYWORD_ONLY
)

#: Keywords that belong to `SystemHost` rather than the config (`info=`,
#: `initializer=`, ...). Derived from the signature too, so a hostctl release
#: that adds one does not turn it into a spurious "unknown argument" here.
_HOST_OPTIONS = frozenset(
    name
    for name, parameter in _inspect.signature(_PosixHost.__init__).parameters.items()
    if parameter.kind is _inspect.Parameter.KEYWORD_ONLY
) | {"client"}


class TrueNASHost(_PosixHost, _ty.Generic[ApiVersion]):
    """A TrueNAS middleware host: POSIX semantics over composed transports.

    Everything generic -- ``run``, ``path``, ``spawn``, ``info``, ``connect``,
    ``close``, ``shell``, ``capabilities``, ``last_selection`` -- is inherited
    from :class:`hostctl.host.PosixHost`, which selects between the providers
    assembled below. What this class adds is only the part no other host has:
    the middleware JSON-RPC websocket and the API surface built on it.

    Construct it from a connection string, a :class:`TrueNASConfig`, or nothing
    at all (the local middleware socket)::

        TrueNASHost("wss://nas")
        TrueNASHost("nas", credentials="1-...", executor=["ssh"])
        TrueNASHost(TrueNASConfig.from_target("wss://nas"))
        TrueNASHost()

    A string accepts every form :class:`~pytruenas.TrueNASClient` does and takes
    the same keyword options as :meth:`TrueNASConfig.from_target`.

    Provider order depends on the target, and is overridable per selector with
    ``executor=``/``path=``:

    * **local** -- hostctl's stock ``local`` pair, and nothing else. Reaching
      this same machine over SSH, a PTY, or the filesystem API would be slower
      and strictly less capable.
    * **remote** -- ``ssh`` then ``webshell`` for commands, ``sftp`` then
      ``tnasws`` for paths. SSH leads on capability; the websocket legs follow.
      This reproduces :class:`~pytruenas.fs.truenas.TruenasPath`'s hand-rolled
      fallback through hostctl's selector, which additionally records a redacted
      trace of what was tried (``host.last_selection``).
    """

    config_type = TrueNASConfig

    def __init__(
        self,
        config: "TrueNASConfig | str | None" = None,
        credentials: object = None,
        *,
        client: object = None,
        **options: object,
    ) -> None:
        # `TrueNASClient(target, creds)` passed credentials positionally, and
        # that is the single most common call in the wild -- accept it.
        if credentials is not None:
            if "credentials" in options:
                raise TypeError("credentials given both positionally and by keyword")
            options["credentials"] = credentials
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
        self._conn: "_connection.TrueNASWSConnection | None" = None
        self.logger = _resolve_logger(config.logger, config.name)
        #: Providers already reported as fallen back from (see `run`), so the
        #: warning is logged once per provider rather than on every call.
        self._fallback_warned: "set[str]" = set()
        #: Guards opening, replacing and dropping `_conn`. Reentrant: logging
        #: in calls `auth.*` through `api`, which reads `conn` again.
        self._conn_lock = _threading.RLock()
        #: How the session last authenticated -- `login()`'s arguments -- so a
        #: reconnect repeats *that* login, not whatever the config would do.
        self._last_login: "tuple[object, dict] | None" = None
        #: Closes the websocket if this host is collected without close().
        self._conn_finalizer: "_weakref.finalize | None" = None
        #: One warning per host about credentials over plaintext ws://.
        self._plaintext_warned = False
        #: Cached SFTP backend, keyed on the SSH settings (see fs.truenas).
        self._sftp_backend_cache: "tuple[str, object] | None" = None
        #: HTTP(S) session for the side channels; see `_http`.
        self._http_session: "_req.Session | None" = None
        # `client=` is accepted and ignored: the host *is* the client now.
        # Kept so existing callers (and tests that injected a stand-in) do not
        # break on an unexpected keyword.
        del client

        executors, paths = self._build_providers(config)
        super().__init__(
            config,
            executor_providers=executors,
            path_providers=paths,
            **_ty.cast(_ty.Any, options),
        )

    def _default_provider_names(self, config: "TrueNASConfig"):
        """The provider names for a target, when nothing is overridden.

        A local target is served entirely by hostctl's stock local pair: plain
        subprocess and plain local paths. Reaching this same machine through
        SSH, a PTY, or the filesystem API would be slower and strictly less
        capable, so no remote provider is offered -- they are all ways of
        reaching a machine somewhere *else*.

        Remotely, SSH leads on capability (separate streams, real stdin, a rich
        POSIX path surface) and the websocket legs follow: the web shell as a
        command channel for a host with no reachable SSH, and ``tnasws`` for
        paths.
        """
        if config.is_local:
            return ("local",), ("local",)
        executors = ("ssh", "webshell") if config.ssh is not None else ("webshell",)
        paths = ("sftp", "tnasws") if config.ssh is not None else ("tnasws",)
        return executors, paths

    def _build_providers(self, config: "TrueNASConfig"):
        """Build the ordered provider tuples for this host.

        ``config.executors`` / ``config.paths`` override the defaults when set,
        naming providers in preference order. That is what makes "force SSH",
        "never use the web shell", or "websocket only" expressible without a
        flag per transport.
        """
        default_executors, default_paths = self._default_provider_names(config)
        explicit_executors = config.executors is not None
        explicit_paths = config.paths is not None
        executor_names = (
            default_executors if config.executors is None else config.executors
        )
        path_names = default_paths if config.paths is None else config.paths

        _reject_unknown(executor_names, EXECUTOR_NAMES, "executor")
        _reject_unknown(path_names, PATH_NAMES, "path")

        # An SSH leg needs asyncssh, which is the optional `ssh` extra. Decide
        # that BEFORE building anything: the defaults offer ssh/sftp whenever a
        # config.ssh exists, which asks whether SSH is *configured* and never
        # whether it is *importable*. Without this, `install_sshcreds()` --
        # which sets config.ssh and rebuilds -- hands a working client a broken
        # SFTP provider, and the next `path()` dies on the import.
        #
        # Only DEFAULTS degrade. A caller who named "ssh"/"sftp" explicitly gets
        # the ImportError: silently serving a different transport than the one
        # asked for is its own bug, and quieter than the failure it replaces.
        if not _ssh_available():
            if not explicit_executors:
                executor_names = tuple(n for n in executor_names if n != "ssh")
            if not explicit_paths:
                path_names = tuple(n for n in path_names if n != "sftp")

        # Both SSH providers come from one factory call so they share a single
        # transport: assembling them by hand type-checks but can silently open
        # two connections, only one of which is ever closed.
        ssh_pair = None
        if "ssh" in executor_names or "sftp" in path_names:
            if config.ssh is None:
                raise ValueError(
                    "ssh/sftp providers were requested but no SSH configuration "
                    "is set; pass ssh=SshConfig(...) or call install_sshcreds()"
                )
            from hostctl import ssh_providers

            ssh_pair = ssh_providers(_ty.cast(_ty.Any, config.ssh))

        local_pair = None
        if "local" in executor_names or "local" in path_names:
            from .providers import local_providers

            local_pair = local_providers()

        def _executor(name: str):
            if name == "local":
                return _ty.cast(_ty.Any, local_pair)[0]
            if name == "ssh":
                # None only when the name survived the filter above -- i.e. the
                # caller asked for it explicitly. Dropped here rather than
                # returned as None so the tuple never holds a hole.
                if ssh_pair is None:
                    return None
                return _ty.cast(_ty.Any, ssh_pair)[0]
            from .webshell import WebShellExecutorProvider

            return WebShellExecutorProvider(_ty.cast(_ty.Any, self))

        def _path(name: str):
            if name == "local":
                return _ty.cast(_ty.Any, local_pair)[1]
            if name == "sftp":
                if ssh_pair is None:
                    return None
                return _ty.cast(_ty.Any, ssh_pair)[1]
            from .providers import TnasWsPathProvider

            # `self` rather than the client: the provider only needs it lazily,
            # which keeps construction free of a websocket connection.
            return TnasWsPathProvider(_ty.cast(_ty.Any, self))

        # Filtering None keeps a half-built SSH pair from putting a hole in the
        # provider tuple, which would fail later and further from the cause.
        return (
            tuple(p for p in map(_executor, executor_names) if p is not None),
            tuple(p for p in map(_path, path_names) if p is not None),
        )

    # -- the TrueNAS surface ----------------------------------------------

    @property
    def _target(self):
        """The resolved websocket target as a :class:`~pytruenas.utils.target.Target`.

        Built from the config rather than stored, so a change that resolves the
        scheme or API path later is picked up without re-syncing two copies.
        """
        config = self._config
        if config.is_local:
            # Encoded, not interpolated raw: `Target.parse` unquotes what it
            # reads, so a socket path holding a "?" or "#" was truncated there
            # (`/run/a?b/x.sock` became `/run/a`). Nothing reads this branch's
            # path today -- `_openwss` uses `config.socket_path` directly -- but
            # a property that renders a wrong path is a trap for whoever does.
            socket_path = config.socket_path or DEFAULT_SOCKET_PATH
            return _TGT.parse(
                f"ws+unix://{_quote_uri_path(socket_path)}", scheme="ws+unix"
            )
        scheme = "ws" if config.secure is False else "wss"
        authority = config.host
        if ":" in authority and not authority.startswith("["):
            # An IPv6 literal: without brackets its colons read as a port.
            authority = f"[{authority}]"
        if config.port:
            authority = f"{authority}:{config.port}"
        api_path = config.api_path or f"/api/{config.version}"
        return _TGT.parse(f"{scheme}://{authority}{api_path}", scheme=scheme)

    @property
    def client(self):
        """Deprecated alias for ``self``.

        The host *is* the client -- they were two objects forwarding halves of
        their surface to each other, which is now one class. Kept so
        ``host.client.api`` and similar keep working.
        """
        return self

    # -- middleware connection ---------------------------------------------

    def _openwss(self):
        config = self._config
        # A unix socket is addressed by its path as given, not re-parsed as a
        # URI: `None` here meant "the default socket", so a configured
        # `socket_path` was silently ignored.
        uri = (
            _connection._UNIX_PREFIX + (config.socket_path or DEFAULT_SOCKET_PATH)
            if config.is_local
            else self._target.uri
        )
        return _connection.TrueNASWSConnection(
            uri,
            verify_ssl=self._config.sslverify,
            py_exceptions=False,
            # Share the host's name-bound logger, so a record from the
            # connection layer names the host it came from -- with several
            # clients open at once, an unattributed "connection was closed" is
            # not actionable.
            logger=self.logger,
        )

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

    def _drop_conn(self, conn: "_connection.TrueNASWSConnection | None") -> None:
        """Discard ``conn`` so the next :attr:`conn` access reconnects.

        Only if it is still the current connection -- another thread may have
        replaced it already -- and closed, not just forgotten: a dropped
        reference used to leak its socket and reader thread.
        """
        with self._conn_lock:
            if conn is not None and self._conn is conn:
                self._conn = None
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass

    @property
    def websocket(self) -> "_connection.TrueNASWSConnection":
        """Former name of :attr:`conn`, kept because it is public API.

        Defined as a property that *reads* ``self.conn`` rather than as
        ``websocket = conn``: the latter makes two independent class
        attributes, so patching or overriding one would silently leave the
        other pointing at the original.
        """
        return self.conn

    def login(
        self,
        creds: "_auth.Credentials | None" = None,
        *,
        login_ex: bool = False,
        login_options: "dict | None" = None,
        otp_provider: "_ty.Callable[[], str] | None" = None,
    ):
        """Open a fresh connection and authenticate.

        By default uses the legacy ``auth.login``/``login_with_*`` path. Pass
        ``login_ex=True`` for the modern mechanism, which supports 2FA via an
        ``OTP_REQUIRED`` continuation: the OTP comes from the credential's own
        ``otp_token`` if set, else from ``otp_provider()``. A credential with no
        login_ex form (e.g. local-socket auth) falls back automatically.

        Refused credentials raise :class:`~pytruenas.auth.AuthenticationError`
        on both paths, and the connection is closed rather than left open and
        unauthenticated. After a success, a reconnect repeats this login; a
        one-time OTP cannot be replayed, so give a session that must survive a
        reconnect an ``otp_provider``.
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
            self._last_login = (creds, options)
            return result

    @_cached_property
    def api(self) -> "ApiVersion":
        """The root API namespace (``host.api.<namespace>.<method>(...)``).

        Parameterise the host to type it: ``TrueNASHost[Current]("nas").api``
        completes exactly as the old ``TrueNASClient[Current]`` did.
        """
        return _ty.cast("ApiVersion", _Namespace(_ty.cast(_ty.Any, self)))

    @property
    def ssh(self):
        """The underlying ``asyncssh`` connection (requires the ``ssh`` extra).

        For the rare caller that needs the raw connection -- port forwarding,
        an SFTP client of its own. Ordinary command and path work should go
        through :meth:`run` and :meth:`path`, which pick a transport rather
        than assuming this one exists.
        """
        for provider in self._executor_selector.providers:
            transport = getattr(provider, "transport", None)
            if transport is not None and hasattr(transport, "ssh"):
                return transport.ssh
        raise RuntimeError(
            "no SSH transport is configured for this host; pass shell=... or "
            "ssh=SshConfig(...), or call install_sshcreds()"
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

    def subscribe(
        self,
        event: str,
        callback: "_ty.Callable[..., object] | None" = None,
        *,
        maxsize: int = _connection.DEFAULT_EVENT_QUEUE_SIZE,
    ):
        """Subscribe to a middleware event; return a ``Subscription``.

        ``host.subscribe("alert.list")`` is shorthand for
        ``host.api.alert.list.subscribe()``. A subscription is bound to the
        current websocket and does **not** survive a reconnect -- the
        ``events()`` iterator ending is that signal.
        """
        return self.conn.subscribe(event, callback, maxsize=maxsize)

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

        The target's port is kept (a ``wss://nas:8443`` API means
        ``https://nas:8443`` side channels; it used to be dropped, sending
        uploads, downloads, file reads, the web shell -- and their auth tokens
        -- to 443). On the NAS itself (the unix-socket target) the side channels
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
        self, file: "str | bytes", method: str, *params, token=None, wait=True, **kwargs
    ):
        """Upload ``file`` via ``/_upload``, then call ``method`` with it."""
        target = self._http_target("/_upload")
        data = {"method": method, "params": params}
        if isinstance(file, str):
            file = file.encode()

        if not token:
            # See the web shell: the server defaults match_origin to True and
            # this token is used once, by one HTTP request from this machine.
            token = self.api.auth.generate_token(5, {}, True, True, **kwargs)

        resp = self._http.post(
            target.uri,
            headers={"Authorization": f"Token {token}"},
            verify=self._http_verify,
            files={"data": _js.dumps(data).encode(), "file": file},
        )
        # An upload the middleware refuses answers with an HTTP error and an
        # HTML/JSON body; without these checks that surfaced as a KeyError or a
        # JSON decode error, naming neither the status nor the reason.
        resp.raise_for_status()
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

    #: Job states after which a job never changes again.
    JOB_DONE = ("SUCCESS", "FAILED", "ABORTED")

    def job_updates(
        self,
        job_id: int,
        *,
        timeout: "float | None" = None,
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
        callback: "_ty.Callable[[dict], object] | None" = None,
        timeout: "float | None" = None,
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
        filename: "str | None" = None,
        buffered=False,
        wait=True,
        **kwargs,
    ):
        """Call ``method`` for a download link and fetch it over HTTP(S)."""
        jobid, link = self.api.core.download(
            method, args, filename or "download", buffered, **kwargs
        )
        target = self._http_target(link)

        if wait:
            if buffered:
                self.wait(jobid, callback=wait if callable(wait) else None)
            resp = self._http.get(target.uri, verify=self._http_verify)
            resp.raise_for_status()
            return resp.content
        return jobid

    def dump_api(self):
        """Run ``middlewared --dump-api`` on the target and parse the JSON."""
        import json

        from .models.apidump import Api

        api: Api = json.loads(
            self.run("middlewared --dump-api", capture_output=True).stdout
        )
        return api

    def install_sshcreds(
        self, name: "str | None" = None, private_key: "str | None" = None
    ):
        """Provision an SSH keypair and wire it into this host's SSH transport.

        Generates (or reuses) a ``SSH_KEY_PAIR`` keychain credential, installs
        the public half on root's ``authorized_keys``, and stores the private
        half on :attr:`TrueNASConfig.ssh` as a real
        :class:`hostctl.host.SshConfig` -- with ``client_keys`` as an actual
        field rather than the ``"client_keys|root"`` string that the pre-hostctl
        client packed into a username.

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
        pubkey: "str | None" = None
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
            # `DbAction.execute`); the tuple says "match on this field name",
            # which is what selecting root by username means.
            self.api.user._upsert(
                ("username",), username="root", sshpubkey="\n".join(authorized)
            )

        private_key = _ty.cast(str, keypair["attributes"]["private_key"])

        from hostctl.host import SshConfig

        # A local target has no host to SSH *to*, and needs none -- commands
        # already run here. The keypair is still provisioned (it is installed
        # on root's authorized_keys, so other machines can use it), but there
        # is no leg to wire it into.
        if self._config.is_local:
            return private_key

        existing = self._config.ssh
        if existing is None:
            self._config.ssh = SshConfig(
                host=self._config.host,
                username="root",
                client_keys=[private_key.encode()],
                known_hosts=_ty.cast(_ty.Any, self._config.known_hosts),
            )
        elif not existing.password and not existing.client_keys:
            existing.client_keys = [private_key.encode()]
        else:
            # Explicit credentials win: a caller who configured their own auth
            # is not silently overridden by a provisioning call.
            return private_key

        from hostctl.provider import ProviderSelector

        executors, paths = self._build_providers(self._config)
        with self._conn_lock:
            # Under the lock, and closing what is replaced: the two selectors
            # were swapped one after the other (so a concurrent call could see
            # a half-swapped pair), and the transports they dropped -- an open
            # SSH connection among them -- were never closed.
            replaced = (self._executor_selector, self._path_selector)
            self._executor_selector = ProviderSelector(executors)
            self._path_selector = ProviderSelector(paths)
            # The SFTP backend is cached per client and keyed on the SSH
            # settings, which just changed; drop it so the next path call does
            # not authenticate with the previous credentials.
            self._sftp_backend_cache = None
        for selector in replaced:
            for provider in getattr(selector, "providers", ()):
                _close_provider(provider)
        return private_key

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

    def run(self, *cmds, **options):
        """Run a command -- :meth:`hostctl.host.PosixHost.run`, plus a warning.

        When the preferred executor cannot start (an SSH leg that is
        unreachable or whose host key is not trusted) hostctl quietly serves
        the call from the next one, usually the web shell. That downgrade is
        worth knowing about, so it is logged once per provider.
        """
        try:
            return super().run(*cmds, **options)
        finally:
            self._warn_fallback()

    def _warn_fallback(self) -> None:
        trace = self.last_selection
        if not trace or trace[0].get("chosen"):
            return
        first = str(trace[0].get("provider"))
        chosen = next((str(t["provider"]) for t in trace if t.get("chosen")), None)
        if chosen is None or first in self._fallback_warned:
            return
        self._fallback_warned.add(first)
        self.logger.warning(
            "run() fell back from %s to %s: %s. If the SSH host key is not in "
            "known_hosts, add it, or pass known_hosts=None to skip the check",
            first,
            chosen,
            trace[0].get("reason") or "unavailable",
        )

    @property
    def name(self) -> str:
        """This host's short label -- see :attr:`TrueNASConfig.name`."""
        return self._config.name

    @property
    def sslverify(self) -> "bool | str":
        """TLS verification for this host -- see :attr:`TrueNASConfig.sslverify`.

        Read from the config rather than stored, so every transport -- the
        JSON-RPC connection, the REST calls, and the web shell -- answers from
        the one value the caller set, with no second copy to drift.
        """
        return self._config.sslverify

    @property
    def _http(self) -> "_req.Session":
        """The HTTP(S) session behind the side channels (upload, download).

        With verification on, HTTPS trusts exactly what the API websocket
        does (see :mod:`pytruenas.utils.tls`).
        """
        if self._http_session is None:
            session = _req.Session()
            context = _tls.context(self._config.sslverify)
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
        return bool(self._config.sslverify)

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


__all__ = ["AUTO_SCHEME", "DEFAULT_SOCKET_PATH", "TrueNASConfig", "TrueNASHost"]
