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

The scheme and API-path probes that :class:`TrueNASClient` historically ran
inside ``__init__`` are *recorded* here (:attr:`~TrueNASConfig.needs_scheme_probe`,
:attr:`~TrueNASConfig.needs_path_probe`) and performed later, on connect.
"""

from __future__ import annotations

import typing as _ty
from urllib.parse import unquote as _unquote
from urllib.parse import urlsplit as _urlsplit

from hostctl.host import HostConfig as _HostConfig
from hostctl.host import PosixHost as _PosixHost
from hostctl.host import uri_host as _uri_host

from . import auth as _auth
from .jsonrpc import DEFAULT_UNIX_SOCKET

if _ty.TYPE_CHECKING:  # pragma: no cover - typing only
    from hostctl.host import Host

#: The local middleware unix socket. Re-exported from :mod:`pytruenas.jsonrpc`
#: rather than redefined, so the two can never drift apart.
DEFAULT_SOCKET_PATH = DEFAULT_UNIX_SOCKET

#: Scheme meaning "probe on first connect" -- a real registered scheme, not a
#: placeholder. It preserves the historical behavior of resolving ws vs wss (and
#: the API path) by asking the server, just deferred out of construction.
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
        sslverify: bool = True,
        credentials: object = None,
        ssh: object = None,
    ) -> None:
        super().__init__()
        self.host = host
        self.port = int(port or 0)
        #: ``True`` -> wss, ``False`` -> ws, ``None`` -> probe on connect.
        self.secure = secure
        self.socket_path = socket_path
        self.api_path = api_path
        self.version = version
        self.sslverify = sslverify
        self.ssh = ssh
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
        "sslverify",
        "ssh",
        "version",
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
            socket_path = parsed.path or f"/{parsed.netloc}"
            return cls(
                socket_path=socket_path or DEFAULT_SOCKET_PATH,
                credentials=creds,
                sslverify=_ty.cast(bool, credentials.get("sslverify", True)),
                version=_ty.cast(str, credentials.get("version", "current")),
                ssh=credentials.get("ssh"),
            )

        secure = None
        if scheme == "truenas+ws":
            secure = False
        elif scheme == "truenas+wss":
            secure = True

        path = parsed.path or ""
        return cls(
            host=parsed.hostname or "",
            port=parsed.port or 0,
            secure=secure,
            api_path=path if path.strip("/") else None,
            credentials=creds,
            sslverify=_ty.cast(bool, credentials.get("sslverify", True)),
            version=_ty.cast(str, credentials.get("version", "current")),
            ssh=credentials.get("ssh"),
        )

    # -- derived state -----------------------------------------------------

    @property
    def is_local(self) -> bool:
        """Whether this target is the local middleware unix socket."""
        return self.socket_path is not None

    @property
    def needs_scheme_probe(self) -> bool:
        """Whether ws-vs-wss still has to be resolved against the server."""
        return not self.is_local and self.secure is None

    @property
    def needs_path_probe(self) -> bool:
        """Whether the API path still has to be resolved against the server."""
        return not self.is_local and self.api_path is None

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


class TrueNASHost(_PosixHost):
    """A TrueNAS middleware host: POSIX semantics over composed transports.

    Everything generic -- ``run``, ``path``, ``spawn``, ``info``, ``connect``,
    ``close``, ``shell``, ``capabilities``, ``last_selection`` -- is inherited
    from :class:`hostctl.host.PosixHost`, which selects between the providers
    assembled below. What this class adds is only the part no other host has:
    the middleware JSON-RPC websocket and the API surface built on it.

    Provider order is deliberate and mirrors today's behaviour:

    * executors -- SSH first (the only remote command channel the JSON-RPC API
      offers is none at all), then the middleware unix socket, which is usable
      only when this process runs on the NAS itself.
    * paths -- SFTP first for its richer POSIX surface (symlinks, rename,
      realpath), then the ``filesystem.*`` websocket, which is always reachable
      but narrower. That reproduces :class:`~pytruenas.fs.truenas.TruenasPath`'s
      hand-rolled fallback through hostctl's selector, which additionally
      records a redacted trace of what was tried (``host.last_selection``).
    """

    config_type = TrueNASConfig

    def __init__(
        self,
        config: "TrueNASConfig | None" = None,
        *,
        client: object = None,
        **options: object,
    ) -> None:
        config = config if config is not None else TrueNASConfig.from_target(None)
        # The client owns the websocket and the api namespace; the host owns
        # transport selection. They reference each other, so the client is
        # built lazily on first use unless one is injected (tests do inject).
        self._client = client
        self._config = config

        executors, paths = self._build_providers(config)
        super().__init__(
            config,
            executor_providers=executors,
            path_providers=paths,
            **_ty.cast(_ty.Any, options),
        )

    def _build_providers(self, config: "TrueNASConfig"):
        from .providers import MiddlewareExecutorProvider, TnasWsPathProvider

        executors: list = []
        paths: list = []

        if config.ssh is not None:
            from hostctl import ssh_providers

            # One call, one shared transport. Assembling the two providers by
            # hand type-checks but can silently open two connections, only one
            # of which is ever closed -- which is why hostctl exposes the pair
            # as a factory rather than exporting the transport.
            executor, path = ssh_providers(_ty.cast(_ty.Any, config.ssh))
            executors.append(executor)
            paths.append(path)

        # `self` is passed rather than the client: the providers only need it
        # lazily, and this keeps construction free of a websocket connection.
        executors.append(MiddlewareExecutorProvider(_ty.cast(_ty.Any, self)))
        paths.append(TnasWsPathProvider(_ty.cast(_ty.Any, self)))
        return tuple(executors), tuple(paths)

    # -- the TrueNAS surface ----------------------------------------------

    @property
    def client(self):
        """The :class:`~pytruenas.TrueNASClient` backing this host's API."""
        if self._client is None:
            from .client import TrueNASClient

            self._client = TrueNASClient._from_config(self._config)
        return self._client

    @property
    def api(self):
        """The root API namespace (``host.api.<namespace>.<method>(...)``)."""
        return self.client.api

    @property
    def websocket(self):
        """The live JSON-RPC websocket, connecting on first access."""
        return self.client.websocket

    def login(self, *args, **kwargs):
        return self.client.login(*args, **kwargs)

    def logout(self) -> None:
        self.client.logout()

    def me(self) -> dict:
        return self.client.me()

    def ping(self) -> str:
        return self.client.ping()

    def subscribe(self, *args, **kwargs):
        return self.client.subscribe(*args, **kwargs)

    def upload(self, *args, **kwargs):
        return self.client.upload(*args, **kwargs)

    def download(self, *args, **kwargs):
        return self.client.download(*args, **kwargs)

    def dump_api(self):
        return self.client.dump_api()

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
        """
        private_key = self.client.install_sshcreds(name=name, private_key=private_key)
        if private_key is None:
            private_key = self.client._ssh_private_key()
        if private_key is None:
            return None

        from hostctl.host import SshConfig

        existing = self._config.ssh
        if existing is None:
            self._config.ssh = SshConfig(
                host=self._config.host,
                username="root",
                client_keys=[private_key.encode()],
            )
        elif not existing.password and not existing.client_keys:
            existing.client_keys = [private_key.encode()]
        else:
            # Explicit credentials win: a caller who configured their own auth
            # is not silently overridden by a provisioning call.
            return private_key

        executors, paths = self._build_providers(self._config)
        from hostctl.provider import ProviderSelector

        self._executor_selector = ProviderSelector(executors)
        self._path_selector = ProviderSelector(paths)
        return private_key

    def close(self) -> None:
        """Close the transports, then the websocket.

        Order matters: the middleware path provider talks over the websocket,
        so it must be torn down before the connection it depends on.
        """
        try:
            super().close()
        finally:
            client = self._client
            if client is not None:
                conn = getattr(client, "_conn", None)
                if conn is not None:
                    try:
                        conn.close()
                    except Exception:
                        # close() must be safe to call repeatedly and must not
                        # mask an error raised by the provider teardown above.
                        pass


__all__ = ["AUTO_SCHEME", "DEFAULT_SOCKET_PATH", "TrueNASConfig", "TrueNASHost"]
