from functools import cached_property
import logging
import subprocess
from pathlib import PurePath, PurePosixPath
import typing as _ty
import io as _io
import warnings
import requests as _req
import json as _js

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
        self._api = _TGT.parse(target or "localhost", scheme="wss", path="/api/current")
        if self._api.username or self._api.password:
            if not creds:
                creds = f"{self._api.username}:{self._api.password}"
            self._api = self._api._replace(username="", password="")
        self._creds = _auth.Credentials(creds)
        self._conn: _conn.JSONRPCClient = None
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

    @property
    def websocket(self):
        if self._conn is None or self._conn._closed.is_set():
            if self.autologin:
                self.login()
            else:
                self._conn = _conn.Client(self._api.uri, verify_ssl=self.sslverify)
        return self._conn

    def login(self, creds: _auth.Credentials = None):
        if self._conn and not self._conn._closed.is_set():
            self._conn.close()
        self._conn = _conn.Client(self._api.uri, verify_ssl=self.sslverify)
        creds = creds or self._creds
        creds.login(self)

    @cached_property
    def api(self) -> "ApiVersion":
        return Namespace(self)

    def upload(self, file: str | bytes, method: str, *params, token=None, wait=True):
        client: "TrueNASClient[Current]" = self

        scheme = "https" if client._api.scheme == "wss" else "http"
        target = client._api._replace(scheme=scheme, path="/_upload", port=0)
        data = {"method": method, "params": params}
        if isinstance(file, str):
            file = file.encode()

        if not token:
            token = client.api.auth.generate_token(5, "params", False)

        resp = _req.post(
            target.uri,
            headers={"Authorization": f"Token {token}"},
            verify=client.sslverify,
            files={"data": _js.dumps(data).encode(), file: file},
        )
        jobid = resp.json()["job_id"]
        if wait:
            client.api.core.job_wait(jobid, job=True)

        return jobid

    def download(self, method: str, *attrs, filename: str = None):
        client: "TrueNASClient[Current]" = self

        scheme = "https" if client._api.scheme == "wss" else "http"
        target = client._api._replace(scheme=scheme, path="/_download", port=0)

        jobid, link = client.api.core.download(
            method, *attrs, filename=filename or "download"
        )

        target = client._api._replace(path=link)

        resp = _req.get(
            target.uri,
            verify=client.sslverify,
        )
        return resp.content

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
        capture_output: bool = False,
        check: bool = False,
        encoding: str | None = None,
        errors: str | None = None,
        input: Input | None = None,
        timeout: float | None = None,
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
                    print(e)
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
        self.logger.trace(f"Running Command: {script}")

        command = [executable, "-c", script]

        match self.shell.scheme:
            case "local":
                result = subprocess.run(
                    command,
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
                )
            case "ssh":
                command = shlex.join(command)
                if cwd:
                    command = f"{shlex.join(['cd', cwd])}; {command}"
                connect_opts = {}
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

                async def _run():
                    async with _ssh.connect(
                        self.shell.host,
                        port=self.shell.port or 22,
                        username=username,
                        known_hosts=None,
                        **connect_opts,
                    ) as conn:
                        result = await conn.run(
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
                    return result

                result = _utils.async_to_sync(_run())
            case _:
                raise NotImplementedError(self.shell.scheme)
        return result
