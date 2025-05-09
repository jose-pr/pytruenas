import functools as _ftools
import io as _io
import json as _js
import os as _os
import pathlib as _path
import subprocess as _localprocess
import sys as _sys
import typing as _ty

import asyncssh as _ssh
import requests as _req

try:
    import pwd as _pwd
except ImportError:
    _pwd = None
import shlex as _shlex

from . import _conn
from . import auth as _auth
from . import fs as _fs
from . import shell as _shell
from .namespace import Namespace
from .utils import async_ as _async
from .utils import io as _ioutils
from .utils import logging as _logging
from .utils.target import Target as _TGT

FileHandle = None | int | _ty.IO
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
        if not logger:
            logger = _logging.getLogger("pytruenas")
        self.logger = _logging.getLogger(logger) if isinstance(logger, str) else logger
        self._api = _TGT.parse(target or "localhost", scheme="auto")
        self.fsbackend = fsbackend

        if self._api.scheme == "auto":
            if self._api.is_local and not self._api.port:
                self._api = self._api._replace(scheme="ws")
            else:
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
            if self._api.is_local and not self._api.port:
                self._api = self._api._replace(path="/websocket")
            else:
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

        shell_ = _TGT.parse(
            shell or "",
            scheme="local" if self._api.is_local else "ssh",
            host=self._api.host,
        )
        if shell_.scheme == "ssh":
            self.shell = _shell.SSHShell(shell_, self.logger)
        elif shell_.scheme == "local":
            self.shell = _shell.LocalShell(shell_.path, self.logger)
        else:
            raise ValueError(shell)

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
        username = client.api.auth.me()["pw_name"]
        user = client.api.user._get(username=username) or {}
        authorizedkeys: list[str] = (user.get("sshpubkey") or "").splitlines()

        if pubkey not in authorizedkeys:
            authorizedkeys.append(pubkey)
            client.api.user._upsert(user["id"], sshpubkey="\n".join(authorizedkeys))

        shell = self.shell
        if isinstance(shell, _shell.SSHShell):
            if not shell.target.username or not shell.target.password:
                shell.target = shell.target._replace(
                    username=f"client_keys|{username}",
                    password=keypair["attributes"]["private_key"],  # type: ignore
                )

    @property
    def sftp(self):
        shell = self.shell
        if not isinstance(shell, _shell.SSHShell):
            raise TypeError(shell)

        if (
            not self._sftp
            or not self._sftp._handler._writer
            or self._sftp._handler._writer._chan._close_event.is_set()
        ):
            self.logger.debug("Openning SFTP channel")
            self._sftp = _async.async_to_sync(shell.conn.start_sftp_client())
        return self._sftp

    def path(self, *path: _fs.PathLike, **kwargs):
        kwargs["backend"] = kwargs.get("backend" or self.fsbackend)
        return _fs.Path(*path, **kwargs, client=self)  # type:ignore

    def run(
        self,
        *cmds,
        bufsize: int = -1,
        stdin: FileHandle | Input = None,
        stdout: FileHandle = None,
        stderr: FileHandle = None,
        cwd: "_fs.PathLike | None" = None,
        env: _ty.Mapping | None = None,
        capture_output: str | bool = True,
        check: bool = True,
        encoding: str | None = None,
        errors: str | None = None,
        timeout: float | None = None,
        loglevel: int = _logging.TRACE,  # type:ignore
    ) -> _localprocess.CompletedProcess:

        return self.shell.run(
            *cmds,
            bufsize=bufsize,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            cwd=cwd,
            env=env,
            capture_output=capture_output,
            check=check,
            encoding=encoding,
            errors=errors,
            timeout=timeout,
            loglevel=loglevel,
        )
