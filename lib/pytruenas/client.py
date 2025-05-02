import functools as _ftools
import io as _io
import json as _js
import logging as _logging
import os as _os
import pathlib as _path
import subprocess as _localprocess
import sys as _sys
import typing as _ty
import warnings as _warn

import asyncssh as _ssh
import requests as _req

try:
    import pwd as _pwd
except ImportError:
    _pwd = None
import shlex as _shlex

from . import _conn
from . import auth as _auth
from .fs import Path
from .namespace import Namespace
from .utils import async_ as _async
from .utils import io as _ioutils
from .utils.target import Target as _TGT

_warn.filterwarnings(action="ignore", module=".*asyncssh.*")


FileHandle = None | int | _ty.IO
PathLike = str | _path.PurePath
Input = bytes | str

if _ty.TYPE_CHECKING:
    from truenasapi_typings.current import Current

    ApiVersion = _ty.TypeVar(
        "ApiVersion", bound=Namespace, default=Current  # type:ignore
    )
else:
    ApiVersion = _ty.TypeVar(
        "ApiVersion",
        bound=Namespace,
    )


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
    ) -> None:
        self._api = _TGT.parse(target or "localhost", scheme="auto")
        self.fsbackend = fsbackend

        if self._api.scheme == "auto":
            resp = _req.get(
                _TGT(
                    scheme="http",
                    username="",
                    password="",
                    host=self._api.host,
                    port=self._api.port,
                    path="",
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

        if not self._api.path:
            for path in ["/api/current", "/websocket"]:
                resp = _req.get(
                    _TGT(
                        scheme=self._api.scheme.replace("ws", "http"),
                        username="",
                        password="",
                        host=self._api.host,
                        port=self._api.port,
                        path=path,
                    ).uri,
                    verify=False,
                )
                if resp.status_code == 400:
                    self._api = self._api._replace(path=path)
                    break

        if self._api.username or self._api.password:
            if not creds:
                creds = f"{self._api.username}:{self._api.password}"
            self._api = self._api._replace(username="", password="")
        self._creds = _auth.Credentials(creds)
        self._conn: _conn.Client | None = None
        self._ssh: _ssh.SSHClientConnection | None = None  # type:ignore
        self._sftp: _ssh.SFTPClient | None = None  # type:ignore
        self.sslverify = sslverify
        self.autologin = autologin
        self.shell = _TGT.parse(
            shell or "",
            scheme="local" if self._api.is_local else "ssh",
            host=self._api.host,
        )
        if not logger:
            logger = _logging.getLogger("pytruenas")
        self.logger = _logging.getLogger(logger) if isinstance(logger, str) else logger

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

    def login(self, creds: _auth.Credentials | None = None):
        if self._conn and not self._conn._closed.is_set():
            self._conn.close()
        self._conn = self._openwss()
        creds = creds or self._creds
        creds.login(self)  # type:ignore

    @_ftools.cached_property
    def api(self) -> "ApiVersion":
        return Namespace(self)  # type:ignore

    def upload(
        self, file: str | bytes, method: str, *params, token=None, wait=True, **kwargs
    ):
        client: "TrueNASClient[Current]" = self  # type:ignore

        scheme = "https" if client._api.scheme == "wss" else "http"
        target = client._api._replace(scheme=scheme, path="/_upload", port=0)
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
            client.api.core.job_wait(jobid, job=True)

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
        client: "TrueNASClient[Current]" = self  # type:ignore

        scheme = "https" if client._api.scheme == "wss" else "http"

        jobid, link = client.api.core.download(
            method, args, filename or "download", buffered, **kwargs
        )  # type:ignore

        target = client._api._replace(scheme=scheme, path=link, port=0)

        if wait:
            if buffered:

                client.api.core.job_wait(jobid, job=True)

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
        client: "TrueNASClient[Current]" = self  # type:ignore
        name = name or "pytruenas"
        keypair = client.api.keychaincredential._get(type="SSH_KEY_PAIR", name=name)
        if not keypair and not private_key:
            private_key = client.api.keychaincredential.generate_ssh_key_pair()[
                "private_key"
            ]  # type:ignore
        elif not private_key:
            private_key = keypair["attributes"]["private_key"]  # type: ignore

        pubkey = (
            _ssh.import_private_key(private_key)  # type:ignore
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
            root.get("sshpubkey") or ""  # type:ignore
        ).splitlines()  # type:ignore

        if pubkey not in rootauthkeys:
            rootauthkeys.append(pubkey)
            client.api.user._upsert(
                "username", username="root", sshpubkey="\n".join(rootauthkeys)
            )
        if not client.shell.username or not client.shell.password:
            client.shell = client.shell._replace(
                username="client_keys|root",
                password=keypair["attributes"]["private_key"],  # type: ignore
            )

    @property
    def ssh(self):
        if not self._ssh or self._ssh._close_event.is_set():
            self.logger.debug("Openning SSH connection")

            connect_opts = {}
            username = ""
            if self.shell.username:
                if "|" in self.shell.username:
                    logintype, username = self.shell.username.split("|", maxsplit=1)
                else:
                    logintype = "password"
                    username = "root"
                creds = self.shell.password
                if logintype == "client_keys" and isinstance(creds, str):
                    creds = creds.encode()
                connect_opts[logintype] = creds
            username = username or "root"
            self._ssh = _async.async_to_sync(
                _ssh.connect(  # type:ignore
                    self.shell.host,
                    port=self.shell.port or 22,
                    username=username,
                    known_hosts=None,
                    **connect_opts,
                )
            )
        return self._ssh

    @property
    def sftp(self):
        if (
            not self._sftp
            or not self._sftp._handler._writer
            or self._sftp._handler._writer._chan._close_event.is_set()
        ):
            self.logger.debug("Openning SFTP channel")
            self._sftp = _async.async_to_sync(self.ssh.start_sftp_client())
        return self._sftp

    def path(self, *path: PathLike, **kwargs):
        kwargs["backend"] = kwargs.get("backend" or self.fsbackend)
        return Path(*path, **kwargs, client=self)  # type:ignore

    def run(
        self,
        *cmds,
        bufsize: int = -1,
        executable: str | None = None,
        stdin: FileHandle = None,
        stdout: FileHandle = None,
        stderr: FileHandle = None,
        cwd: PathLike | None = None,
        env: _ty.Mapping | None = None,
        capture_output: str | bool = True,
        check: bool = True,
        encoding: str | None = None,
        errors: str | None = None,
        input: Input | None = None,
        timeout: float | None = None,
        loglevel: int = _logging.TRACE,  # type:ignore
    ) -> _localprocess.CompletedProcess:

        if not executable:
            if self.shell.path:
                executable = self.shell.path
            else:
                try:
                    if self._api.is_local and _pwd:
                        executable = _pwd.getpwnam("root").pw_shell
                    else:
                        executable = self.api.user._get(username="root")["shell"]  # type: ignore
                except Exception as e:
                    self.logger.warning(
                        "Count not get default shell for root, using bash as default"
                    )
                    executable = "/bin/bash"

        script = []
        for cmd in cmds:
            if not isinstance(cmd, (tuple, list)):
                if isinstance(cmd, (_path.PurePath, Path)):
                    cmd = _shlex.quote(cmd.as_posix())
                elif isinstance(cmd, _os.PathLike):
                    cmd = _shlex.quote(_os.fspath(cmd))
                else:
                    cmd = str(cmd)
            else:
                cmd = " ".join(_shellquote(c) for c in cmd)
            script.append(cmd)

        if cwd:
            cwd = _path.PurePosixPath(cwd).as_posix()

        script = ";".join(script)
        if loglevel:
            self.logger.log(loglevel, f"Running Command: {script}")

        command = [executable, "-c", script]

        match (capture_output or ""):
            case "stdout":
                stdout = _localprocess.PIPE
            case "stderr":
                stderr = _localprocess.PIPE
            case True:
                if not stderr:
                    stderr = _localprocess.PIPE
                if not stdout:
                    stdout = _localprocess.PIPE

        if input:
            if stdin is not None:
                raise ValueError("stdin")

        if _ioutils.isbytelike(stdin) or isinstance(stdin, str):
            input = _ty.cast(bytes, stdin)
            stdin = None

        if isinstance(input, str):
            input = input.encode()

        match self.shell.scheme:
            case "local":
                if stdin and not isinstance(stdin, int):
                    try:
                        readme = stdin.fileno() == -1
                    except (OSError, AttributeError):
                        if not hasattr(stdin, "read"):
                            raise TypeError(stdin)
                        readme = True
                    if readme:
                        input = stdin.read()
                        stdin = None

                result = _localprocess.run(
                    command,
                    bufsize=bufsize,
                    input=input,
                    stdin=stdin,
                    stdout=stdout,
                    stderr=stderr,
                    cwd=cwd,
                    env=env,
                    check=check,
                    encoding=encoding,
                    errors=errors,
                    timeout=timeout,
                )
            case "ssh":
                command = _shlex.join(command)
                if cwd:
                    command = f"{_shlex.join(['cd', cwd])}; {command}"

                if stdout in (None, _localprocess.STDOUT, _sys.stdout):
                    stdout = open(_os.dup(_sys.stdout.fileno()), _sys.stdout.mode)
                if stderr in (None, _sys.stderr):
                    stderr = open(_os.dup(_sys.stderr.fileno()), _sys.stderr.mode)

                if input:
                    stdin = _io.BytesIO(input)

                result = _async.async_to_sync(
                    self.ssh.run(
                        command,
                        bufsize=bufsize,
                        stdin=stdin,
                        stdout=stdout,
                        stderr=stderr,
                        env=env,
                        check=check,
                        encoding=encoding,
                        errors=errors,
                        timeout=timeout,
                    )
                )
            case _:
                raise NotImplementedError(self.shell.scheme)
        return _ty.cast(_localprocess.CompletedProcess, result)


def _shellquote(c: object):
    if isinstance(c, _os.PathLike):
        if hasattr(c, "as_posix"):
            c = c.as_posix()  # type:ignore
        else:
            c = _os.fspath(c)
        c = _shlex.quote(c)  # type:ignore
    elif isinstance(c, bytes):
        c = c.decode()
    else:
        c = _shlex.quote(str(c))
    return c
