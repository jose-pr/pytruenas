from functools import cached_property
import logging
import subprocess
from pathlib import PurePath, PurePosixPath
import typing as _ty
import io as _io
import warnings

warnings.filterwarnings(action="ignore", module=".*asyncssh.*")

import asyncssh as _ssh
import urllib.parse

try:
    import pwd
except ImportError:
    pass
import shlex

from . import _conn, _utils
from . import auth as _auth
from .namespace import Namespace

FileHandle = None | int | _ty.IO
PathLike = str | PurePath
Input = bytes | str


class ShellConfig:
    def __init__(self, *configs, **fields):
        _config = {}

        for config in reversed([*configs, fields]):
            config = config or {}
            if isinstance(config, str):
                parsed = urllib.parse.urlsplit("ssh://" + config)
                config = {
                    "hostname": parsed.hostname,
                    "logintype": urllib.parse.unquote(parsed.username or ""),
                    "credentials": urllib.parse.unquote(parsed.password or ""),
                    "port": parsed.port,
                    "path": parsed.path,
                }
            for k, v in config.items():
                _config.setdefault(k, v)

        self.hostname = _config.get("hostname")
        self.logintype = _config.get("logintype")
        self.credentials = _config.get("credentials")
        self.port = _config.get("port")
        self.path = _config.get("path")


ApiVersion = _ty.TypeVar("ApiVersion", bound=Namespace)


class TrueNASClient(_ty.Generic[ApiVersion]):
    def __init__(
        self,
        target: str = None,
        creds: "tuple[str,str]|str|dict" = None,
        autologin=True,
        sslverify=True,
        *,
        api=None,
        shell=None,
        logger: logging.Logger = None,
    ) -> None:
        self._target = target or "localhost"
        self._creds = _auth.Credentials(creds)
        self._conn: _conn.JSONRPCClient = None
        self.sslverify = sslverify
        self.autologin = autologin
        self.api_uri = api or self._target
        self.shell = ShellConfig(shell)
        if not logger:
            logger = logging.getLogger("pytruenas")
        self.logger = logging.getLogger(logger) if isinstance(logger, str) else logger

    def _is_local(self):
        return self._target.lower() in ["localhost", "127.0.0.1"]

    @property
    def api_uri(self):
        return self._api

    @api_uri.setter
    def api_uri(self, value: str):
        if not value or value.lower() in ["localhost", "127.0.0.1"]:
            self._api = None
        else:
            self._api = f"wss://{value}/api/current"

    @property
    def conn(self):
        if self._conn is None or self._conn._closed.is_set():
            if self.autologin:
                self.login()
            else:
                self._conn = _conn.Client(self.api_uri, verify_ssl=self.sslverify)
        return self._conn

    def login(self, creds: _auth.Credentials = None):
        if self._conn and not self.conn._closed.is_set():
            self._conn.close()
        self._conn = _conn.Client(self.api_uri, verify_ssl=self.sslverify)
        creds = creds or self._creds
        creds.login(self)

    @cached_property
    def api(self) -> "ApiVersion":
        return Namespace(self)

    def dump_api(self):
        import json
        from .models.apidump import Api

        api: Api = json.loads(
            self.run("middlewared --dump-api", capture_output=True).stdout
        )
        return api

    def install_sshcreds(self, name: str = None, private_key: str = None):
        name = name or "pytruenas"
        keypair = self.api.keychaincredential._get(type="SSH_KEY_PAIR", name=name)
        if not keypair and not private_key:
            private_key = self.api.keychaincredential.generate_ssh_key_pair()[
                "private_key"
            ]
        elif not private_key:
            private_key = keypair["attributes"]['private_key']

        pubkey = _ssh.import_private_key(private_key).export_public_key().decode().strip()

        keypair = self.api.keychaincredential._upsert(
            "name",
            ("update_exclude", ["type"]),
            type="SSH_KEY_PAIR",
            name=name,
            attributes={"private_key": private_key, 'public_key':pubkey},
        )
        root = self.api.user._get(username="root")
        rootauthkeys = (root.get("sshpubkey") or "").splitlines()

        if pubkey not in rootauthkeys:
            rootauthkeys.append(pubkey)
            self.api.user._upsert(
                "username", username="root", sshpubkey="\n".join(rootauthkeys)
            )

        self.shell.logintype = "client_keys"
        self.shell.credentials = keypair["attributes"]["private_key"]

    def run(
        self,
        *cmds,
        bufsize: int = -1,
        executable: str | None = None,
        stdin: FileHandle = None,
        stdout: FileHandle = None,
        stderr: FileHandle = None,
        env: _ty.Mapping | None = None,
        capture_output: bool = False,
        check: bool = False,
        encoding: str | None = None,
        errors: str | None = None,
        input: Input | None = None,
        timeout: float | None = None,
    ) -> subprocess.CompletedProcess:
        is_local = self._is_local()

        if not executable:
            if self.shell.path:
                executable = self.shell.path
            else:
                try:
                    if is_local:
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

        command = [executable, "-c", ";".join(script)]

        if is_local:
            result = subprocess.run(
                command,
                bufsize=bufsize,
                stdin=stdin,
                stdout=stdout,
                stderr=stderr,
                env=env,
                capture_output=capture_output,
                check=check,
                encoding=encoding,
                errors=errors,
                timeout=timeout,
            )
        else:
            command = shlex.join(command)

            connect_opts = {}
            if self.shell.logintype:
                creds = self.shell.credentials
                if self.shell.logintype == "client_keys" and isinstance(creds, str):
                    creds = creds.encode()
                connect_opts[self.shell.logintype] = creds

            async def _run():
                async with _ssh.connect(
                    self.shell.hostname or self._target,
                    port=self.shell.port or 22,
                    username="root",
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
        return result
