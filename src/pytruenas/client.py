from __future__ import annotations

from functools import cached_property
import logging as _logging
import subprocess
from pathlib import PurePath
import typing as _ty
import warnings
import requests as _req
import json as _js

warnings.filterwarnings(action="ignore", module=".*asyncssh.*")


from . import _conn
from .jsonrpc import DEFAULT_UNIX_SOCKET as _DEFAULT_SOCKET_PATH
from .utils.target import Target as _TGT
from . import auth as _auth
from .namespace import Namespace

FileHandle = _ty.Union[None, int, _ty.IO]
PathLike = _ty.Union[str, PurePath]
Input = _ty.Union[bytes, str]

if _ty.TYPE_CHECKING:
    from truenasapi_typings.current import Current

    ApiVersion = _ty.TypeVar(
        "ApiVersion", bound=Namespace, default=Current  # type: ignore
    )
else:
    ApiVersion = _ty.TypeVar(
        "ApiVersion",
        bound=Namespace,
    )


def _asyncssh():
    """Import ``asyncssh`` on demand (the optional ``ssh`` extra)."""
    try:
        import asyncssh
    except ImportError as exc:  # pragma: no cover - only without the extra
        raise ImportError(
            "SSH/SFTP support requires the 'ssh' extra: pip install pytruenas[ssh]"
        ) from exc
    return asyncssh


class TrueNASClient(_ty.Generic[ApiVersion]):
    def __init__(
        self,
        target: str | None = None,
        creds: "tuple[str,str]|str|dict|None" = None,
        autologin=True,
        sslverify=True,
        *,
        shell: str | None = None,
        logger: _logging.Logger | None = None,
        fsbackend: "str|_ty.Sequence[str]" = "auto",
        version: str = "current",
    ) -> None:
        self._api = _TGT.parse(target or "localhost", scheme="auto")
        self.fsbackend = fsbackend

        if self._api.scheme == "auto":
            if not (self._api.is_local and not self._api.port):
                resp = _req.get(
                    _TGT(
                        scheme="http",
                        username="",
                        password="",
                        host=self._api.host,
                        port=self._api.port,
                        path="",
                        query="",
                        fragment="",
                    ).uri,
                    verify=False,
                )

                self._api = self._api._replace(
                    scheme=(
                        "wss"
                        if _TGT.parse(resp.url, scheme="http").scheme == "https"
                        else "ws"
                    )
                )
            else:
                self._api = self._api._replace(scheme="ws")

        if not self._api.path:
            if not (self._api.is_local and not self._api.port):

                for path in [f"/api/{version}", "/websocket"]:
                    resp = _req.get(
                        _TGT(
                            scheme=self._api.scheme.replace("ws", "http"),
                            username="",
                            password="",
                            host=self._api.host,
                            port=self._api.port,
                            path=path,
                            query="",
                            fragment="",
                        ).uri,
                        verify=False,
                    )
                    if resp.status_code == 400:
                        self._api = self._api._replace(path=path)
                        break
            else:
                self._api = self._api._replace(path="/websocket")

        if self._api.username or self._api.password:
            if not creds:
                creds = f"{self._api.username}:{self._api.password}"
            self._api = self._api._replace(username="", password="")
        self._creds = _auth.Credentials(creds)
        self._conn: _conn.Client | None = None
        self.sslverify = sslverify
        self.autologin = autologin
        # Built lazily by `.host`; `_config` is also set directly by
        # `_from_config` when a TrueNASHost owns the configuration.
        self._host = None
        self._config = None
        #: Connection target for the SSH leg of `.run()`/`.path()`.
        #:
        #: Renamed from `.shell` in the hostctl migration: `Host.shell` there is
        #: the *bound shell object* (`host.shell.run(...)`), and keeping a
        #: connection target under that name would have collided with it for
        #: every consumer of the new API.
        self.ssh_config = _TGT.parse(
            shell or "",
            scheme="local" if self._api.is_local else "ssh",
            host=self._api.host,
        )
        if not logger:
            logger = _logging.getLogger("pytruenas")
        self.logger = _logging.getLogger(logger) if isinstance(logger, str) else logger

    @classmethod
    def _from_config(cls, config, *, autologin: bool = True, logger=None):
        """Build a client from an already-parsed :class:`~pytruenas.host.TrueNASConfig`.

        The config layer has already done the URI work, so this deliberately
        does **not** re-parse a target string: it maps the resolved fields onto
        the client's own state. Used by
        :class:`~pytruenas.host.TrueNASHost`, which owns the config and needs a
        client for the API surface.

        Any scheme/path still marked for probing stays unresolved here -- the
        probe happens on first connect, which is what keeps construction free of
        network I/O.
        """
        if config.is_local:
            target = None
        else:
            scheme = "ws" if config.secure is False else "wss"
            authority = config.host
            if config.port:
                authority = f"{authority}:{config.port}"
            # A path is always supplied, even when the config has not resolved
            # one: `__init__` probes for a missing path over HTTP, which would
            # make building the client hit the network -- exactly the thing the
            # config layer exists to defer. The default matches what that probe
            # settles on first.
            api_path = config.api_path or f"/api/{config.version}"
            target = f"{scheme}://{authority}{api_path}"

        client = cls(
            target,
            config.credentials,
            autologin=autologin,
            sslverify=config.sslverify,
            logger=logger,
            version=config.version,
        )
        client._config = config
        return client

    def _openwss(self):
        return _conn.Client(
            None if self._api.is_local and not self._api.port else self._api.uri,
            verify_ssl=self.sslverify,
            py_exceptions=False,
        )

    @property
    def websocket(self):
        if self._conn is None or self._conn._closed.is_set():
            if self.autologin:
                self.login()
            else:
                self._conn = self._openwss()
        return _ty.cast(_conn.Client, self._conn)

    def login(
        self,
        creds: _auth.Credentials | None = None,
        *,
        login_ex: bool = False,
        login_options: "dict | None" = None,
        otp_provider: "_ty.Callable[[], str] | None" = None,
    ):
        """Open a fresh connection and authenticate.

        By default uses the legacy ``auth.login``/``login_with_*`` path
        (unchanged). Pass ``login_ex=True`` to use the modern ``auth.login_ex``
        mechanism instead -- which supports 2FA via an ``OTP_REQUIRED``
        continuation: the OTP comes from the credential's own ``otp_token`` if
        set, else from ``otp_provider()`` if given. ``login_options`` overrides
        the server defaults (``{"user_info": True, "reconnect_token": False}``).
        A credential with no login_ex form (e.g. local-socket auth) falls back
        to the legacy path automatically.
        """
        if self._conn and not self._conn._closed.is_set():
            try:
                self._conn.close()
            except Exception:
                pass
        self._conn = self._openwss()
        creds = creds or self._creds
        if login_ex:
            return creds.login_ex(  # type: ignore
                self, login_options=login_options, otp_provider=otp_provider
            )
        creds.login(self)  # type: ignore

    @cached_property
    def api(self) -> "ApiVersion":
        return Namespace(self)  # type: ignore

    # -- convenience wrappers over common auth/core methods -----------------

    def me(self) -> "dict":
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
        callback: "_ty.Callable[[_conn.Event], object] | None" = None,
        *,
        maxsize: int = _conn.DEFAULT_EVENT_QUEUE_SIZE,
    ) -> "_conn.Subscription":
        """Subscribe to a middleware event; return a :class:`Subscription`.

        ``client.subscribe("alert.list")`` is the client-level shorthand for
        ``client.api.alert.list.subscribe()``. Consume via the returned
        subscription's ``events()`` iterator and/or ``callback`` (inline on the
        reader thread -- keep it fast). Note a subscription is bound to the
        current websocket connection and does NOT survive a reconnect; re-
        subscribe if the connection drops (the ``events()`` iterator ends on
        disconnect, signalling exactly that).
        """
        return self.websocket.subscribe(event, callback, maxsize=maxsize)

    def _http_target(self, path: str):
        """The host's HTTP(S) URL for ``path`` (the websocket ``ws/wss`` scheme
        mapped to ``http/https``), used by the upload/download side channels."""
        scheme = "https" if self._api.scheme == "wss" else "http"
        return self._api._replace(scheme=scheme, path=path, port=0)

    def upload(
        self, file: str | bytes, method: str, *params, token=None, wait=True, **kwargs
    ):
        client: "TrueNASClient[Current]" = self  # type: ignore

        target = client._http_target("/_upload")
        data = {"method": method, "params": params}
        if isinstance(file, str):
            file = file.encode()

        if not token:
            token = client.api.auth.generate_token(5, {}, False, **kwargs)

        resp = _req.post(
            target.uri,
            headers={"Authorization": f"Token {token}"},
            verify=client.sslverify,
            files={"data": _js.dumps(data).encode(), "file": file},
        )
        jobid = resp.json()["job_id"]
        if wait:
            client.api.core.job_wait(jobid, job=True, _timeout=None)

        return jobid

    def download(
        self,
        method: str,
        *args,
        filename: str | None = None,
        buffered=False,
        wait=True,
        **kwargs,
    ):
        client: "TrueNASClient[Current]" = self  # type: ignore

        jobid, link = client.api.core.download(
            method, args, filename or "download", buffered, **kwargs
        )  # type: ignore

        target = client._http_target(link)

        if wait:
            if buffered:

                client.api.core.job_wait(jobid, job=True, _timeout=None)

            resp = _req.get(
                target.uri,
                verify=client.sslverify,
            )
            resp.raise_for_status()
            return resp.content

        return jobid

    def dump_api(self):
        import json
        from .models.apidump import Api

        api: Api = json.loads(
            self.run("middlewared --dump-api", capture_output=True).stdout
        )
        return api

    def install_sshcreds(self, name: str | None = None, private_key: str | None = None):
        client: "TrueNASClient[Current]" = self  # type: ignore
        name = name or "pytruenas"
        keypair = client.api.keychaincredential._get(type="SSH_KEY_PAIR", name=name)
        if not keypair and not private_key:
            private_key = client.api.keychaincredential.generate_ssh_key_pair()[
                "private_key"
            ]  # type: ignore
        elif not private_key:
            private_key = keypair["attributes"]["private_key"]  # type: ignore

        pubkey = (
            _asyncssh()
            .import_private_key(private_key)  # type: ignore
            .export_public_key()
            .decode()
            .strip()
        )

        keypair = client.api.keychaincredential._upsert(
            ("name", "type"),
            type="SSH_KEY_PAIR",
            name=name,
            attributes={"private_key": private_key, "public_key": pubkey},
        )
        root = client.api.user._get(username="root")
        rootauthkeys: list[str] = (
            root.get("sshpubkey") or ""  # type: ignore
        ).splitlines()  # type: ignore

        if pubkey not in rootauthkeys:
            rootauthkeys.append(pubkey)
            client.api.user._upsert(
                "username", username="root", sshpubkey="\n".join(rootauthkeys)
            )
        installed = _ty.cast(str, keypair["attributes"]["private_key"])  # type: ignore
        if not client.ssh_config.username or not client.ssh_config.password:
            client.ssh_config = client.ssh_config._replace(
                username="client_keys|root",
                password=installed,
            )
        # Returned so a caller holding the config (TrueNASHost) can store the
        # key on a real SshConfig instead of re-reading the packed username.
        return installed

    def _ssh_private_key(self) -> "str | None":
        """The private key configured for SSH auth, if key-based auth is in use.

        A small accessor over how the credential happens to be stored, so
        callers (and tests) do not depend on the ``client_keys|root`` encoding
        packed into ``shell.username``. That encoding is what the hostctl
        migration replaces with ``SshConfig``'s real ``client_keys`` field --
        see ``.agents/plans/hostctl_host_migration.md`` step 5.
        """
        username = self.ssh_config.username or ""
        if "|" not in username:
            return None
        logintype, _, _ = username.partition("|")
        if logintype != "client_keys":
            return None
        password = self.ssh_config.password
        if isinstance(password, bytes):
            return password.decode()
        return password

    # -- delegated to hostctl -------------------------------------------
    #
    # `run`, `path`, and the asyncssh connection used to live here as ~200
    # lines of shell quoting, local-vs-ssh branching, and stdin/capture
    # normalization. That is all generic host behaviour, and hostctl now owns
    # it: `TrueNASHost` composes an SSH transport with the middleware ones and
    # inherits `run`/`path`/`spawn` from `hostctl.host.PosixHost`.
    #
    # The methods below keep `TrueNASClient`'s signatures working by forwarding
    # to that host. Equivalence was verified on a real POSIX target (TrueNAS
    # 26.0.0-BETA.1): every assertion in the ported run() suite passes
    # identically against both implementations.

    @property
    def host(self):
        """The :class:`~pytruenas.host.TrueNASHost` backing this client.

        Built lazily from this client's own configuration, so importing or
        constructing a client never opens a transport.
        """
        if self._host is None:
            from .host import TrueNASHost

            self._host = TrueNASHost(self._as_config(), client=self)
        return self._host

    def _as_config(self):
        """This client's settings as a :class:`~pytruenas.host.TrueNASConfig`.

        A client built the legacy way (a target string parsed in ``__init__``)
        has already resolved its scheme and path, so the config is constructed
        from the resolved values rather than re-parsing the original string.
        """
        if self._config is not None:
            return self._config

        from .host import TrueNASConfig

        api = self._api
        if api.is_local and not api.port:
            config = TrueNASConfig(
                socket_path=_DEFAULT_SOCKET_PATH,
                credentials=self._creds,
                sslverify=self.sslverify,
            )
        else:
            config = TrueNASConfig(
                host=api.host,
                port=api.port,
                secure=api.scheme == "wss",
                api_path=api.path or None,
                credentials=self._creds,
                sslverify=self.sslverify,
            )
        config.ssh = self._as_ssh_config()
        self._config = config
        return config

    def _as_ssh_config(self):
        """An :class:`hostctl.host.SshConfig` from ``.ssh_config``, or ``None``.

        ``None`` means no SSH leg: the host then has only the middleware
        transports, which for a *remote* target means no ``run`` capability at
        all. That is not a regression -- it is the pre-existing situation made
        visible, since the JSON-RPC API exposes no remote command execution.
        """
        shell = self.ssh_config
        host = getattr(shell, "host", None)
        if not host or shell.scheme == "local":
            return None

        from hostctl.host import SshConfig

        username = shell.username or ""
        password = shell.password or None
        client_keys = None
        if "|" in username:
            logintype, username = username.split("|", maxsplit=1)
            if logintype == "client_keys" and password:
                client_keys = [
                    password.encode() if isinstance(password, str) else password
                ]
                password = None
        return SshConfig(
            host=host,
            port=shell.port or 22,
            username=username or "root",
            password=password,
            client_keys=client_keys,
            executable=shell.path or None,
        )

    @property
    def ssh(self):
        """The underlying asyncssh connection (requires the ``ssh`` extra)."""
        provider = self.host._executor_selector.providers[0]
        transport = getattr(provider, "transport", None)
        if transport is None:
            raise RuntimeError("no SSH transport is configured for this client")
        return transport.ssh

    def path(self, *path: PathLike, backend: "str | None" = None):
        from .fs import path as _make_path

        return _make_path(self, *path, backend=backend or self.fsbackend)

    def run(self, *cmds, **kwargs) -> subprocess.CompletedProcess:
        """Run commands on the target; see :meth:`hostctl.host.Host.run`.

        ``executable`` is accepted for backwards compatibility and forwarded.
        """
        return self.host.run(*cmds, **kwargs)
