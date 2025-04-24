from functools import cached_property
import logging
import subprocess
from pathlib import PurePath, PurePosixPath
import typing as _ty
import io as _io
import warnings
import requests as _req
import json as _js
import sys as _sys
import os as _os

warnings.filterwarnings(action="ignore", module=".*asyncssh.*")

import asyncssh as _ssh

try:
    import pwd
except ImportError:
    pass
import shlex


from . import _conn, _utils
from .utils.target import Target as _TGT
from . import auth as _auth
from .namespace import Namespace
from .fs import Path

FileHandle = None | int | _ty.IO
PathLike = str | PurePath
Input = bytes | str

if _ty.TYPE_CHECKING:
    from truenasapi_typings.current import Current

    ApiVersion = _ty.TypeVar("ApiVersion", bound=Namespace, default=Current)
else:
    ApiVersion = _ty.TypeVar(
        "ApiVersion",
        bound=Namespace,
    )


class TrueNASClient(_ty.Generic[ApiVersion]):
    def __init__(
        self,
        target: str = None,
        creds: "tuple[str,str]|str|dict" = None,
        autologin=True,
        sslverify=True,
        *,
        shell: str = None,
        logger: logging.Logger = None,
    ) -> None:
        self._api = _TGT.parse(
            target or "localhost", scheme="ws" if not target else "wss"
        )

        if not self._api.path:
            path = "/api/current"
            for path in ["/api/current", "/websocket"]:
                resp = _req.get(
                    _TGT(
                        self._api.scheme.replace("ws", "http"),
                        username=None,
                        password=None,
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
        self._conn: _conn.JSONRPCClient = None
        self._ssh: _ssh.SSHClientConnection = None
        self._sftp: _ssh.SFTPClient = None
        self.sslverify = sslverify
        self.autologin = autologin
        self.shell = _TGT.parse(
            shell or "",
            scheme="local" if self._api.is_local else "ssh",
            host=self._api.host,
        )
        if not logger:
            logger = logging.getLogger("pytruenas")
        self.logger = logging.getLogger(logger) if isinstance(logger, str) else logger

    def _openwss(self):
        return _conn.Client(
            self._api.uri, verify_ssl=self.sslverify, py_exceptions=False
        )

    @property
    def websocket(self):
        if self._conn is None or self._conn._closed.is_set():
            if self.autologin:
                self.login()
            else:
                self._conn = self._openwss()
        return self._conn

    def login(self, creds: _auth.Credentials = None):
        if self._conn and not self._conn._closed.is_set():
            self._conn.close()
        self._conn = self._openwss()
        creds = creds or self._creds
        creds.login(self)

    @cached_property
    def api(self) -> "ApiVersion":
        return Namespace(self)

    def upload(
        self, file: str | bytes, method: str, *params, token=None, wait=True, **kwargs
    ):
        client: "TrueNASClient[Current]" = self

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
        filename: str = None,
        buffered=False,
        wait=True,
        **kwargs,
    ):
        client: "TrueNASClient[Current]" = self

        scheme = "https" if client._api.scheme == "wss" else "http"

        jobid, link = client.api.core.download(
            method, args, filename or "download", **kwargs
        )

        target = client._api._replace(scheme=scheme, path=link, port=0)

        if wait:

            if buffered:
                client.api.core.job_wait(jobid, job=True)

            resp = _req.get(
                target.uri,
                verify=client.sslverify,
            )
            return resp.content

        return jobid

    def dump_api(self):
        import json
        from .models.apidump import Api

        api: Api = json.loads(
            self.run("middlewared --dump-api", capture_output=True).stdout
        )
        return api

    def install_sshcreds(self, name: str = None, private_key: str = None):
        client: "TrueNASClient[Current]" = self
        name = name or "pytruenas"
        keypair = client.api.keychaincredential._get(type="SSH_KEY_PAIR", name=name)
        if not keypair and not private_key:
            private_key = client.api.keychaincredential.generate_ssh_key_pair()[
                "private_key"
            ]
        elif not private_key:
            private_key = keypair["attributes"]["private_key"]

        pubkey = (
            _ssh.import_private_key(private_key).export_public_key().decode().strip()
        )

        keypair = client.api.keychaincredential._upsert(
            "name",
            ("update_exclude", ["type"]),
            type="SSH_KEY_PAIR",
            name=name,
            attributes={"private_key": private_key, "public_key": pubkey},
        )
        root = client.api.user._get(username="root")
        rootauthkeys = (root.get("sshpubkey") or "").splitlines()

        if pubkey not in rootauthkeys:
            rootauthkeys.append(pubkey)
            client.api.user._upsert(
                "username", username="root", sshpubkey="\n".join(rootauthkeys)
            )
        if not client.shell.username or not client.shell.password:
            client.shell = client.shell._replace(
                username="client_keys|root",
                password=keypair["attributes"]["private_key"],
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
            self._ssh = _utils.async_to_sync(
                _ssh.connect(
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
            self._sftp = _utils.async_to_sync(self.ssh.start_sftp_client())
        return self._sftp

    def path(self, *path: PathLike, **kwargs):
        return Path(*path, **kwargs, client=self)

    def run(
        self,
        *cmds,
        bufsize: int = -1,
        executable: str | None = None,
        stdin: FileHandle = None,
        stdout: FileHandle = None,
        stderr: FileHandle = None,
        cwd: PathLike = None,
        env: _ty.Mapping | None = None,
        capture_output: str | bool = True,
        check: bool = True,
        encoding: str | None = None,
        errors: str | None = None,
        input: Input | None = None,
        timeout: float | None = None,
        loglevel: int = logging.TRACE,
    ) -> subprocess.CompletedProcess:

        if not executable:
            if self.shell.path:
                executable = self.shell.path
            else:
                try:
                    if self._api.is_local:
                        executable = pwd.getpwnam("root").pw_shell
                    else:
                        executable = self.api.user._get(username="root")["shell"]
                except Exception as e:
                    self.logger.warning(
                        "Count not get default shell for root, using bash as default"
                    )
                    executable = "/bin/bash"

        script = []
        for cmd in cmds:
            if not isinstance(cmd, (tuple, list)):
                if isinstance(cmd, PurePath):
                    cmd = shlex.quote(cmd.as_posix())
                else:
                    cmd = str(cmd)
            else:
                cmd = [a.as_posix() if isinstance(a, PurePath) else str(a) for a in cmd]
                cmd = shlex.join(cmd)
            script.append(cmd)

        if cwd:
            cwd = PurePosixPath(cwd).as_posix()

        script = ";".join(script)
        if loglevel:
            self.logger.log(loglevel, f"Running Command: {script}")

        command = [executable, "-c", script]

        match (capture_output or ""):
            case "stdout":
                stdout = subprocess.PIPE
            case "stderr":
                stderr = subprocess.PIPE
            case True:
                if not stderr:
                    stderr = subprocess.PIPE
                if not stdout:
                    stdout = subprocess.PIPE

        if input:
            if stdin is not None:
                raise ValueError("stdin")

        if _utils.isbytelike(stdin):
            input = stdin
            stdin = None

        if hasattr(stdin, "encode"):
            stdin = stdin.encode()

        match self.shell.scheme:
            case "local":
                if stdin:
                    try:
                        readme = stdin.fileno() == -1
                    except (OSError, AttributeError):
                        if not hasattr(stdin, "read"):
                            raise TypeError(stdin)
                        readme = True
                    if readme:
                        input = stdin.read()
                        stdin = None

                result = subprocess.run(
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
                command = shlex.join(command)
                if cwd:
                    command = f"{shlex.join(['cd', cwd])}; {command}"

                if stdout in (None, subprocess.STDOUT, _sys.stdout):
                    stdout = open(_os.dup(_sys.stdout.fileno()), _sys.stdout.mode)
                if stderr in (None, _sys.stderr):
                    stderr = open(_os.dup(_sys.stderr.fileno()), _sys.stderr.mode)

                if input:
                    stdin = _io.BytesIO(input)

                result = _utils.async_to_sync(
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
        return result
