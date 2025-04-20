from functools import cached_property
import logging
import subprocess
from pathlib import PurePath, PurePosixPath
import typing as _ty
import io as _io
import asyncssh as _ssh

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


class TrueNASClient:
    def __init__(
        self,
        target: str = None,
        creds: "tuple[str,str]|str|dict" = None,
        autologin=True,
        sslverify=True,
        *,
        api=None,
        sshcreds=None,
        logger: logging.Logger = None,
    ) -> None:
        self._target = target or "localhost"
        self._creds = _auth.Credentials(creds)
        self._conn: _conn.JSONRPCClient = None
        self.sslverify = sslverify
        self.autologin = autologin
        self.api_uri = api or self._target
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
            self._conn = _conn.Client(self.api_uri, verify_ssl=self.sslverify)
            if self.autologin:
                self._creds.login(self)
        return self._conn

    @cached_property
    def api(self):
        return Namespace(self)

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
            if not isinstance(cmd, (tuple,list)):
                if isinstance(cmd, PurePath):
                    cmd = shlex.quote(cmd.as_posix())
                else:
                    cmd = str(cmd)
            else:
                cmd = [a.as_posix() if isinstance(a, PurePath) else str(a) for a in cmd]
                cmd = shlex.join(cmd)
            script.append(cmd)

        command = [executable, "-c", ';'.join(script)]

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

            async def _run():
                async with _ssh.connect(self._target) as conn:
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

            result = _utils.async_to_sync(_run)
        return result
