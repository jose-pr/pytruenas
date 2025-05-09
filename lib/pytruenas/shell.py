import io as _io
import os as _os
import shlex as _shlex
import subprocess as _localprocess
import sys as _sys
import typing as _ty

import asyncssh as _ssh

from . import fs as _fs
from .utils import async_ as _async
from .utils import io as _ioutils
from .utils import logging as _logging
from .utils import target as _tgt

Input = bytes | str

CommandResult = _localprocess.CompletedProcess


def _shellquote(c: object):
    if isinstance(c, _os.PathLike):
        c = _shlex.quote(_os.fspath(c))
    elif isinstance(c, bytes):
        c = c.decode()
    else:
        c = _shlex.quote(str(c))
    return c


class Shell(_ty.Protocol):
    def run(
        self,
        *cmds,
        bufsize: int = -1,
        stdin: _ioutils.FileHandle | Input | None = None,
        stdout: _ioutils.FileHandle = None,
        stderr: _ioutils.FileHandle = None,
        cwd: "_fs.PathLike | None" = None,
        env: _ty.Mapping | None = None,
        capture_output: str | bool = True,
        check: bool = True,
        encoding: str | None = None,
        errors: str | None = None,
        timeout: float | None = None,
        loglevel: int = _logging.TRACE,
    ) -> CommandResult: ...


class BaseShell(Shell):

    _LINESEPARATOR: str = ";"

    def __init__(self, shell: str, logger: _logging.Logger) -> None:
        self.shell = shell
        self.logger = logger

    def eval(
        self,
        script: str,
        bufsize: int = -1,
        stdin: _ioutils.FileHandle | bytes = None,
        stdout: _ioutils.FileHandle = None,
        stderr: _ioutils.FileHandle = None,
        cwd: "_fs.PathLike | None" = None,
        env: _ty.Mapping | None = None,
        encoding: str | None = None,
        errors: str | None = None,
        timeout: float | None = None,
    ) -> CommandResult: ...
    def run(
        self,
        *cmds,
        bufsize: int = -1,
        stdin: _ioutils.FileHandle | Input | None = None,
        stdout: _ioutils.FileHandle = None,
        stderr: _ioutils.FileHandle = None,
        cwd: "_fs.PathLike | None" = None,
        env: _ty.Mapping | None = None,
        capture_output: str | bool = True,
        check: bool = True,
        encoding: str | None = None,
        errors: str | None = None,
        timeout: float | None = None,
        loglevel: int = _logging.TRACE,
    ) -> CommandResult:
        script = []
        for cmd in cmds:
            if not isinstance(cmd, (tuple, list)):
                if isinstance(cmd, _os.PathLike):
                    cmd = _shlex.quote(_os.fspath(cmd))
                else:
                    cmd = str(cmd)
            else:
                cmd = " ".join(_shellquote(c) for c in cmd)
            script.append(cmd)

        script = self._LINESEPARATOR.join(script)
        if loglevel:
            self.logger.log(loglevel, f"Running Command: {script}")

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

        if isinstance(stdin, str):
            stdin = stdin.encode()

        result = self.eval(
            script,
            bufsize,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            cwd=cwd,
            env=env,
            encoding=encoding,
            errors=errors,
            timeout=timeout,
        )
        if check and result.returncode != 0:
            raise _localprocess.CalledProcessError(
                result.returncode, script, result.stdout, result.stderr
            )

        return result


class LocalShell(BaseShell):

    def eval(
        self,
        script: str,
        bufsize: int = -1,
        stdin: _ioutils.FileHandle | bytes | None = None,
        stdout: _ioutils.FileHandle = None,
        stderr: _ioutils.FileHandle = None,
        cwd: "_fs.PathLike | None" = None,
        env: _ty.Mapping | None = None,
        encoding: str | None = None,
        errors: str | None = None,
        timeout: float | None = None,
    ) -> CommandResult:
        input: bytes | None = None
        if _ioutils.isbytelike(stdin):
            stdin = None
            input = stdin
        elif stdin and not isinstance(stdin, int):
            try:
                readme = stdin.fileno() == -1  # type:ignore
            except (OSError, AttributeError):
                if not hasattr(stdin, "read"):
                    raise TypeError(stdin)
                readme = True
            if readme:
                input = stdin.read()  # type:ignore
                stdin = None

        return _localprocess.run(
            [self.shell, "-c", script],
            bufsize=bufsize,
            input=input,
            stdin=stdin,  # type:ignore
            stdout=stdout,
            stderr=stderr,
            cwd=cwd,
            env=env,
            check=False,
            encoding=encoding,
            errors=errors,
            timeout=timeout,
        )


def _open_ssh_connection(self: "SSHShell"):
    self.logger.debug("Openning SSH connection")

    connect_opts = {}
    username = ""
    if self.target.username:
        if "|" in self.target.username:
            logintype, username = self.target.username.split("|", maxsplit=1)
        else:
            logintype = "password"
            username = self.target.username
        creds = self.target.password
        if logintype == "client_keys" and isinstance(creds, str):
            creds = creds.encode()
        connect_opts[logintype] = creds
        connect_opts["username"] = username
    return _async.async_to_sync(
        _ssh.connect(  # type:ignore
            self.target.host,
            port=self.target.port or 22,
            known_hosts=None,
            **connect_opts,
        )
    )


class SSHShell(BaseShell):

    def __init__(
        self,
        target: _tgt.Target,
        logger: _logging.Logger,
        connect: _ty.Callable[[_ty.Self], _ssh.SSHClientConnection] | None = None,
    ) -> None:
        self._conn = None
        self.target = target
        self.connect = connect or _open_ssh_connection
        super().__init__(target.path, logger)

    @property
    def conn(self):
        if not self._conn or self._conn._close_event.is_set():
            self._conn = self.connect(self)
        return self._conn

    def eval(
        self,
        script: str,
        bufsize: int = -1,
        stdin: _ioutils.FileHandle | bytes | None = None,
        stdout: _ioutils.FileHandle = None,
        stderr: _ioutils.FileHandle = None,
        cwd: "_fs.PathLike | None" = None,
        env: _ty.Mapping | None = None,
        encoding: str | None = None,
        errors: str | None = None,
        timeout: float | None = None,
    ) -> CommandResult:
        if self.shell:
            command = _shlex.join([self.shell, "-c", script])
        else:
            command = script
        if cwd:
            command = f"{_shlex.join(['cd', _os.fspath(cwd)])}; {command}"

        if stdout in (None, _localprocess.STDOUT, _sys.stdout):
            stdout = open(_os.dup(_sys.stdout.fileno()), _sys.stdout.mode)
        if stderr in (None, _sys.stderr):
            stderr = open(_os.dup(_sys.stderr.fileno()), _sys.stderr.mode)

        if _ioutils.isbytelike(stdin):
            stdin = _io.BytesIO(stdin)

        return _ty.cast(
            CommandResult,
            _async.async_to_sync(
                self.conn.run(
                    command,
                    bufsize=bufsize,
                    stdin=stdin,
                    stdout=stdout,
                    stderr=stderr,
                    env=env,
                    check=False,
                    encoding=encoding,
                    errors=errors,
                    timeout=timeout,
                )
            ),
        )
