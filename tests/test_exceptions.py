"""The error hierarchy: one base in `pytruenas.exceptions`, exported from the root."""

import importlib
import inspect
import pkgutil
import socket
import threading

import pytest

import pytruenas
from pytruenas import TrueNASError, exceptions
from pytruenas.exceptions import (
    APIDumpError,
    AuthenticationError,
    CallTimeout,
    ClientException,
    ConnectError,
    ConnectionClosed,
    FieldError,
    JobFailed,
    UnknownMethod,
    ValidationErrors,
)

_ERRORS = [
    ClientException("[ENOENT] gone", 2),
    ValidationErrors([("user.name", "required", 22)]),
    CallTimeout(),
    ConnectionClosed(sent=False),
    JobFailed({"id": 7, "state": "FAILED", "error": "boom"}),
    ConnectError("refused", 404),
    AuthenticationError("AUTH_ERR", {}),
    APIDumpError("digest mismatch"),
    UnknownMethod("no method named 'x'"),
    FieldError("--x: not a valid integer"),
]


@pytest.mark.parametrize("error", _ERRORS, ids=lambda e: type(e).__name__)
def test_every_runtime_error_is_a_truenas_error(error):
    with pytest.raises(TrueNASError):
        raise error


@pytest.mark.parametrize("error", _ERRORS, ids=lambda e: type(e).__name__)
def test_every_error_is_exported_from_the_root(error):
    name = type(error).__name__
    assert getattr(pytruenas, name) is type(error)
    assert name in pytruenas.__all__
    assert name in exceptions.__all__
    assert "TrueNASError" in pytruenas.__all__


def test_the_existing_bases_still_hold():
    """Code catching `ClientException` keeps catching every call error."""
    for kind in (ValidationErrors, CallTimeout, ConnectionClosed, JobFailed):
        assert issubclass(kind, ClientException)


def test_builtin_bases_say_what_a_caller_already_catches():
    assert issubclass(ValidationErrors, ValueError)
    assert issubclass(FieldError, ValueError)
    assert issubclass(UnknownMethod, LookupError)
    assert issubclass(APIDumpError, RuntimeError)


def _package_errors():
    found = set()
    for info in pkgutil.walk_packages(pytruenas.__path__, "pytruenas."):
        # The typings generator's errors are its own module's to place.
        if info.name.startswith("pytruenas.codegen"):
            continue
        try:
            module = importlib.import_module(info.name)
        except ImportError:  # an optional extra that is not installed
            continue
        for value in vars(module).values():
            if (
                inspect.isclass(value)
                and issubclass(value, BaseException)
                and value.__module__.startswith("pytruenas")
            ):
                found.add(value)
    return found


def test_every_error_the_package_defines_has_one_root_and_one_module():
    errors = _package_errors()
    assert errors, "found no error classes"
    for error in errors:
        assert issubclass(error, TrueNASError), error
        assert error.__module__ == "pytruenas.exceptions", error


def test_no_error_is_an_oserror():
    """`exists()`/`is_dir()` read an `OSError` as "not there": a timeout or a
    dropped connection must not pass for a missing file."""
    for error in _package_errors():
        assert not issubclass(error, OSError), error


def _answer_the_upgrade_with(status_line):
    server = socket.socket()
    server.bind(("127.0.0.1", 0))
    server.listen(1)

    def serve():
        conn, _ = server.accept()
        conn.recv(4096)
        conn.sendall(status_line + b"\r\nContent-Length: 0\r\n\r\n")
        conn.close()
        server.close()

    threading.Thread(target=serve, daemon=True).start()
    return server.getsockname()[1]


def test_a_refused_upgrade_is_a_connect_error():
    """A wrong API path is a 404 on the upgrade; websocket-client's own
    exception crossed the API, and `except TrueNASError` did not catch it."""
    import websocket

    port = _answer_the_upgrade_with(b"HTTP/1.1 404 Not Found")
    client = pytruenas.TrueNASClient(f"ws://127.0.0.1:{port}", autologin=False)
    with pytest.raises(ConnectError) as raised:
        client.api.core.ping()
    assert raised.value.status == 404
    assert "HTTP 404" in str(raised.value)
    assert isinstance(raised.value.__cause__, websocket.WebSocketException)
    client.close()


def test_a_refused_port_stays_an_oserror():
    """An `OSError` that already says what failed is raised as it is."""
    server = socket.socket()
    server.bind(("127.0.0.1", 0))
    port = server.getsockname()[1]
    server.close()
    client = pytruenas.TrueNASClient(f"ws://127.0.0.1:{port}", autologin=False)
    with pytest.raises(ConnectionRefusedError):
        client.api.core.ping()
    client.close()
